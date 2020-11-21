import praw
import config
import time
import os
import urllib.request
from urllib.request import urlopen
import subprocess
from daltonize import d_run
import pyimgur
from os import path
from datetime import datetime

botname = 'u/' + config.botname.lower

def print_d(logmsg):
    """ Prints the given message with a timestamp prepended. """
    now = datetime.now()
    print(str(now) + ": " + logmsg)

def bot_login():
    """ Function for logging in the bot into Reddit. """
    print_d("Logging in...")
    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "Dalton_Bot")
    print_d("Logged in!")
    
    return r

def clean_output_directories():
    """ Function for cleaning up the output directories. """
    if (os.path.isfile("daltonize-this.jpg")):
        os.remove("daltonize-this.jpg")
    if (os.path.isfile(config.output_dir_deuteranopia)):
        os.remove(config.output_dir_deuteranopia)
    if (os.path.isfile(config.output_dir_protanopia)):
        os.remove(config.output_dir_protanopia)
    if (os.path.isfile(config.output_dir_tritanopia)):
        os.remove(config.output_dir_tritanopia)

def process_pms(red):
    """ Function for processing edit requests via pm """

    # Cleanup operation if bot died mid-daltonization.
    clean_output_directories()

    # Create output directory for daltonized images.
    if (not path.exists("daltonized")):
        os.mkdir("daltonized")

    try:
        # Loop through all unread messages in inbox.
        for msg in red.inbox.unread(limit=None):
            # Getting response criterias.
            usernameMention = msg.subject == 'username mention'
            usernameInBody = msg.subject == 'comment reply' and botname in msg.body.lower()
            isCommentReply = msg.was_comment

            # This PM doesn't meet the response criteria. Mark it as 'read' and skip it.
            if not (usernameMention or usernameInBody or not isCommentReply):
                msg.mark_read()
                continue

            # Retrieve the mentioned comment using the message ID.
            mentionedComment = red.comment(msg.id)
            mentionedComment.refresh()

            print_d("Found message from " + msg.author.name + ", contents: " + msg.body)

            # Skips comments where the bot has already made a comment.
            replies = mentionedComment.replies
            skip = False
            for reply in replies:
                if (reply.author.name.lower() == 'dalton-bot'):
                    skip = True
            if (skip):
                print_d("Skipping because already commented")
                msg.mark_read()
                continue

            # Get submission that comment was made on.
            commentPost = mentionedComment.submission
            imageUrl = None
            commentReply = None
            uploaded_image_d = None
            uploaded_image_p = None
            uploaded_image_t = None

            # If submission is a link post.
            if (not commentPost.is_self):
                imageUrl = commentPost.url
            else:
                print_d("Post is a self post.")
                commentReply = "I'm sorry, but I don't work for self posts." + config.footer_text
                make_comment(msg, mentionedComment, commentReply)
                continue

            # If the URL is not null.
            if (imageUrl is not None):
                print_d("This is the post URL: " + imageUrl)

                # Ensures content type of url request is of valid image type.
                image_formats = ("image/png", "image/jpeg", "image/gif", "image/bmp")
                site = urlopen(imageUrl)
                meta = site.info()
                if (meta["content-type"] in image_formats):
                    # Download the image and verify it exists locally.
                    urllib.request.urlretrieve(imageUrl, "daltonize-this.jpg")
                    if (os.path.isfile("daltonize-this.jpg")):
                        print_d("Successfully downloaded image")
                        print_d("Daltonizing...")

                        # Runs the daltonization operation for both deuteranopia and protanopia colourblindness.
                        d_run("daltonize-this.jpg", config.output_dir_deuteranopia, "d");
                        d_run("daltonize-this.jpg", config.output_dir_protanopia, "p");
                        d_run("daltonize-this.jpg", config.output_dir_tritanopia, "t");

                        # Verify daltonized output files exist.
                        if (os.path.isfile(config.output_dir_deuteranopia) and os.path.isfile(config.output_dir_protanopia) and os.path.isfile(config.output_dir_tritanopia)):
                            print_d("Successfully daltonized images")
                            print_d("Uploading to Imgur...")

                            # Upload daltonized images to Imgur.
                            im = pyimgur.Imgur(config.imgur_client_id)
                            uploaded_image_d = im.upload_image(config.output_dir_deuteranopia, title="Uploaded by /u/Dalton-Bot")
                            uploaded_image_p = im.upload_image(config.output_dir_protanopia, title="Uploaded by /u/Dalton-Bot")
                            uploaded_image_t = im.upload_image(config.output_dir_tritanopia, title="Uploaded by /u/Dalton-Bot")
                        else:
                            # The daltonized images were not found, so must have failed during daltonization.
                            print_d("Failed to daltonize. Daltonized images were not found.")
                            commentReply = "I'm sorry, but I was unable to daltonize the image." + config.footer_text
                            make_comment(msg, mentionedComment, commentReply)
                            continue
                    else:
                        # The bot failed to download the image in the post.
                        print_d("Failed to download image. Image file was not found.")
                        commentReply = "I'm sorry, but I was unable to download this image." + config.footer_text
                        make_comment(msg, mentionedComment, commentReply)
                        continue
                else:
                    # The bot couldn't download the image because the post link was not an image.
                    print_d("Failed to download. Post link was not an image.")
                    commentReply = "I'm sorry, but I don't work for links that aren't images." + config.footer_text
                    make_comment(msg, mentionedComment, commentReply)
                    continue

                # If images are uploaded.
                if (uploaded_image_d is not None and uploaded_image_p is not None and uploaded_image_t is not None):
                    print_d("This is the uploaded D-Image: " + uploaded_image_d.link + ", P-Image: " + uploaded_image_p.link + ", T-Image: " + uploaded_image_t.link)
                    commentReply = "Here you go:\n\nDeutan: " + uploaded_image_d.link + "\n\nProtan: " + uploaded_image_p.link + "\n\nTritan: " + uploaded_image_t.link + config.footer_text
                    make_comment(msg, mentionedComment, commentReply)
                    continue
                else:
                    # The bot failed to upload the images to Imgur.
                    print_d("The Imgur links don't exist")
                    commentReply = "I'm sorry, but I was unable to upload the daltonized images to Imgur." + config.footer_text
                    make_comment(msg, mentionedComment, commentReply)
                    continue

            # Make the comment with the imgur links containing the daltonized images.
            make_comment(msg, mentionedComment, commentReply)

    except Exception as e:
        # An error has occured, log the message and retry.
        print_d(str(e))
        if hasattr(e, 'message'):
            print_d(str(e.message))

def make_comment(msg, mentionedComment, commentReply):
    """ Makes a comment on the comment reply, marks the message as read, and cleans the output directories (if needed). """

    if (commentReply is not None):
        # Reply to comment.
        mentionedComment.reply(commentReply)
        print_d('Comment made.\n')

        # Mark the message as read
        msg.mark_read()

        # Clean the output directories (if needed)
        clean_output_directories()
    else:
        print_d("The generated comment was empty, comment was not made.")

r = bot_login()

while True: 
    process_pms(r)
    time.sleep(10)