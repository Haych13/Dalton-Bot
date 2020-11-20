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

botname = 'u/dalton-bot'

def print_d(logmsg):
    """ Prints the given message with a timestamp prepended"""
    now = datetime.now()
    print(str(now) + ": " + logmsg)

def bot_login():
    """ function for logging in the bot into Reddit. """
    print_d("Logging in...")
    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "Dalton_Bot")
    print_d("Logged in!")
    
    return r

def process_pms(red):
    """ Function for processing edit requests via pm """

    # Cleanup operation if bot died mid-daltonization.
    if (os.path.isfile("daltonize-this.jpg")):
        os.remove("daltonize-this.jpg")
    if (os.path.isfile(config.outputdirdeuteranopia)):
        os.remove(config.outputdirdeuteranopia)
    if (os.path.isfile(config.outputdirprotanopia)):
        os.remove(config.outputdirprotanopia)
    if (os.path.isfile(config.outputdirtritanopia)):
        os.remove(config.outputtritanopia)

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

            # If the URL is not null.
            if (imageUrl is not None):
                print_d("This is the post URL: "+ imageUrl)

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
                        d_run("daltonize-this.jpg", config.outputdirdeuteranopia, "d");
                        d_run("daltonize-this.jpg", config.outputdirprotanopia, "p");
                        d_run("daltonize-this.jpg", config.outputdirtritanopia, "t");

                        # Verify daltonized output files exist.
                        if (os.path.isfile(config.outputdirdeuteranopia) and os.path.isfile(config.outputdirprotanopia)) and os.path.isfile(config.outputdirtritanopia)):
                            print_d("Successfully daltonized images")
                            print_d("Uploading to Imgur...")

                            # Upload daltonized images to Imgur.
                            im = pyimgur.Imgur(config.imgur_client_id)
                            uploaded_image_d = im.upload_image(config.outputdirdeuteranopia, title="Uploaded by /u/Dalton-Bot")
                            uploaded_image_p = im.upload_image(config.outputdirprotanopia, title="Uploaded by /u/Dalton-Bot")
                            uploaded_image_t = im.upload_image(config.outputdirtritanopia, title="Uploaded by /u/Dalton-Bot")
                        else:
                            print_d("Failed to daltonize. Daltonized images were not found.")
                    else:
                        print_d("Failed to download image. Image file was not found.")
                else:
                    print_d("Failed to download. Post link was not an image.")

                # If images are uploaded.
                if (uploaded_image_d is not None and uploaded_image_p is not None):
                    print_d("This is the uploaded D-Image: " + uploaded_image_d.link + ", P-Image: " + uploaded_image_p.link + ", T-Image: " + uploaded_image_t.link)
                    commentReply = "Here you go:\n\ndeutan: " + uploaded_image_d.link + "\n\nProtan: " + uploaded_image_p.link + "\n\nTritan: " + uploaded_image_t.link + "\n\n---\n\n^^*I* ^^*am* ^^*a* ^^*bot,* ^^*and* ^^*this* ^^*action* ^^*was* ^^*performed* ^^*automatically.* &#32; ^^| ^^[Subreddit](http://www.reddit.com//r/DaltonBot/)&#32; ^^| ^^[Source](https://gitlab.com/Haych/dalton-bot)"
                else:
                    print_d("The Imgur links don't exist")
            else:
                print_d("Unable to retrieve post url.")

            # If a reply was generated using the Imgur links.
            if (commentReply is not None):
                # Reply to comment.
                mentionedComment.reply(commentReply)
                print_d('Comment made.\n')

                # Mark message as read.
                msg.mark_read()

                # Cleanup operation.
                os.remove("daltonize-this.jpg")
                os.remove(config.outputdirdeuteranopia)
                os.remove(config.outputdirprotanopia)
                os.remove(config.outputdirtritanopia)
            else:
                print_d("Failed to daltonize/upload image. See above reason(s).")
    except Exception as e:
        if hasattr(e, 'message'):
            print_d(str(e.message))
        else:
            print_d(str(e))

r = bot_login()

while True: 
    process_pms(r)
    time.sleep(10)
