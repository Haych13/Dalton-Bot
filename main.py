import praw
import time
from dotenv import load_dotenv
import os
import urllib.request
import logging
from urllib.request import urlopen
import subprocess
from daltonize import d_run, s_run
import pyimgur
from os import path
from datetime import datetime

#Load variables from the .env files
load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
imgur_client_id = os.getenv('IMGUR_CLIENT_ID')
footer_text = os.getenv('FOOTER_TEXT')
d_output_dir_deuteranopia  = os.getenv('D_OUTPUT_DIR_DEUTERANOPIA')
d_output_dir_protanopia = os.getenv('D_OUTPUT_DIR_PROTANOPIA')
d_output_dir_tritanopia = os.getenv('D_OUTPUT_DIR_TRITANOPIA')
s_output_dir_deuteranopia  = os.getenv('S_OUTPUT_DIR_DEUTERANOPIA')
s_output_dir_protanopia = os.getenv('S_OUTPUT_DIR_PROTANOPIA')
s_output_dir_tritanopia = os.getenv('S_OUTPUT_DIR_TRITANOPIA')

# Print the environment variables for testing
print(os.getenv("USERNAME"))
print(os.getenv("PASSWORD"))
print(os.getenv("CLIENT_ID"))
print(os.getenv("CLIENT_SECRET"))
print(os.getenv("IMGUR_CLIENT_ID"))
print(os.getenv("FOOTER_TEXT"))
print(os.getenv("D_OUTPUT_DIR_DEUTERANOPIA"))
print(os.getenv("D_OUTPUT_DIR_PROTANOPIA"))
print(os.getenv("D_OUTPUT_DIR_TRITANOPIA"))
print(os.getenv("S_OUTPUT_DIR_DEUTERANOPIA"))
print(os.getenv("S_OUTPUT_DIR_PROTANOPIA"))
print(os.getenv("S_OUTPUT_DIR_TRITANOPIA"))

#Create botname
botname = 'u/' + username.lower()

def print_d(logmsg):
    """ Prints the given message with a timestamp prepended. """
    now = datetime.now()
    print(str(now) + ": " + logmsg)

def bot_login():
    """ Function for logging in the bot into Reddit. """
    print_d("Logging in...")
    r = praw.Reddit(username = username,
                password = password,
                client_id = client_id,
                client_secret = client_secret,
                user_agent = "Dalton_Bot")
    print_d("Logged in!")

    return r

def clean_output_directories():
    """ Function for cleaning up the output directories. """
    if (os.path.isfile("downloaded-image.jpg")):
        os.remove("downloaded-image.jpg")
    if (os.path.isfile(d_output_dir_deuteranopia)):
        os.remove(d_output_dir_deuteranopia)
    if (os.path.isfile(d_output_dir_protanopia)):
        os.remove(d_output_dir_protanopia)
    if (os.path.isfile(d_output_dir_tritanopia)):
        os.remove(d_output_dir_tritanopia)
    if (os.path.isfile(s_output_dir_deuteranopia)):
        os.remove(s_output_dir_deuteranopia)
    if (os.path.isfile(s_output_dir_protanopia)):
        os.remove(s_output_dir_protanopia)
    if (os.path.isfile(s_output_dir_tritanopia)):
        os.remove(s_output_dir_tritanopia)

def process_pms(red):
    """ Function for processing edit requests via pm """

    # Cleanup operation if bot died mid-daltonization.
    clean_output_directories()

    # Create output directory for daltonized and simulated images.
    if (not path.exists("daltonized")):
        os.mkdir("daltonized")
    if (not path.exists("simulated")):
        os.mkdir("simulated")

    try:
        # Loop through all unread messages in inbox.
        for msg in red.inbox.unread(limit=None):
            # Getting response criterias.
            usernameMention = msg.subject == 'username mention'
            usernameInBody = msg.subject == 'comment reply' and botname in msg.body.lower()
            isCommentReply = msg.was_comment

            daltonize_flag = True if '--d' in msg.body.lower() or 'daltonize' in msg.body.lower() else False
            simulate_flag = True if '--s' in msg.body.lower() or 'simulate' in msg.body.lower() else False

            daltonize_error = False
            simulate_error = False

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
            d_uploaded_image_d = None
            d_uploaded_image_p = None
            d_uploaded_image_t = None
            s_uploaded_image_d = None
            s_uploaded_image_p = None
            s_uploaded_image_t = None

            # If submission is a link post.
            if (not commentPost.is_self):
                imageUrl = commentPost.url
            else:
                print_d("Post is a self post.")
                commentReply = "I'm sorry, but I don't work for self posts." + footer_text
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
                    urllib.request.urlretrieve(imageUrl, "downloaded-image.jpg")
                    if (os.path.isfile("downloaded-image.jpg")):
                        print_d("Successfully downloaded image")
                        # If daltonizing.
                        if (daltonize_flag is False and simulate_flag is False or daltonize_flag is True and simulate_flag is False):
                            daltonize_flag = True
                            print_d("Daltonizing...")
                            # Runs the daltonization operation for deuteranopia, protanopia, and tritanopia colourblindness.
                            d_run("downloaded-image.jpg", d_output_dir_deuteranopia, "d")
                            d_run("downloaded-image.jpg", d_output_dir_protanopia, "p")
                            d_run("downloaded-image.jpg", d_output_dir_tritanopia, "t")

                        # If daltonizing and simulating.
                        elif (daltonize_flag is True and simulate_flag is True):
                            print_d("Daltonizing and simulating...")
                            # Runs the daltonization and simulation operation for deuteranopia, protanopia, and tritanopia colourblindness.
                            d_run("downloaded-image.jpg", d_output_dir_deuteranopia, "d")
                            d_run("downloaded-image.jpg", d_output_dir_protanopia, "p")
                            d_run("downloaded-image.jpg", d_output_dir_tritanopia, "t")
                            s_run("downloaded-image.jpg", s_output_dir_deuteranopia, "d")
                            s_run("downloaded-image.jpg", s_output_dir_protanopia, "p")
                            s_run("downloaded-image.jpg", s_output_dir_tritanopia, "t")

                        # If simulating.
                        elif (daltonize_flag is False and simulate_flag is True):
                            print_d("Simulating...")
                            # Runs the simulation operation for deuteranopia, protanopia, and tritanopia colourblindness.
                            s_run("downloaded-image.jpg", s_output_dir_deuteranopia, "d")
                            s_run("downloaded-image.jpg", s_output_dir_protanopia, "p")
                            s_run("downloaded-image.jpg", s_output_dir_tritanopia, "t")

                        # imgur upload client.
                        im = pyimgur.Imgur(imgur_client_id)
                        if (daltonize_flag is True):
                            if (os.path.isfile(d_output_dir_deuteranopia) and os.path.isfile(d_output_dir_protanopia) and os.path.isfile(d_output_dir_tritanopia)):
                                print_d("Successfully daltonized images")
                                print_d("Uploading daltonized images to Imgur...")
                                d_uploaded_image_d = im.upload_image(d_output_dir_deuteranopia, title="Uploaded by /u/Dalton-Bot")
                                d_uploaded_image_p = im.upload_image(d_output_dir_protanopia, title="Uploaded by /u/Dalton-Bot")
                                d_uploaded_image_t = im.upload_image(d_output_dir_tritanopia, title="Uploaded by /u/Dalton-Bot")
                            else:
                                # The daltonized images were not found, so must have failed during daltonization.
                                print_d("Failed to daltonize. Daltonized images were not found.")
                                commentReply = "I'm sorry, but I was unable to daltonize the image." + footer_text
                                daltonize_error = True

                        if (simulate_flag is True):
                            if (os.path.isfile(s_output_dir_deuteranopia) and os.path.isfile(s_output_dir_protanopia) and os.path.isfile(s_output_dir_tritanopia)):
                                print_d("Successfully simulated images")
                                print_d("Uploading simulated images to Imgur...")
                                s_uploaded_image_d = im.upload_image(s_output_dir_deuteranopia, title="Uploaded by /u/Dalton-Bot")
                                s_uploaded_image_p = im.upload_image(s_output_dir_protanopia, title="Uploaded by /u/Dalton-Bot")
                                s_uploaded_image_t = im.upload_image(s_output_dir_tritanopia, title="Uploaded by /u/Dalton-Bot")
                            else:
                                # The simulated images were not found, so must have failed during simulation.
                                print_d("Failed to simulate. Simulated images were not found.")
                                commentReply = "I'm sorry, but I was unable to daltonize the image." + footer_text
                                simulate_error = True

                    else:
                        # The bot failed to download the image in the post.
                        print_d("Failed to download image. Image file was not found.")
                        commentReply = "I'm sorry, but I was unable to download this image." + footer_text
                        make_comment(msg, mentionedComment, commentReply)
                        continue
                else:
                    # The bot couldn't download the image because the post link was not an image.
                    print_d("Failed to download. Post link was not an image.")
                    commentReply = "I'm sorry, but I don't work for links that aren't images." + footer_text
                    make_comment(msg, mentionedComment, commentReply)
                    continue

                # If an error occurred during daltonization or simulation.
                if (daltonize_error is True or simulate_error is True):
                    make_comment(msg, mentionedComment, commentReply)
                    continue

                # If images are uploaded.
                if (daltonize_flag is True and simulate_flag is True):
                    if (d_uploaded_image_d is not None and d_uploaded_image_p is not None and d_uploaded_image_t is not None and s_uploaded_image_d is not None and s_uploaded_image_p is not None and s_uploaded_image_t is not None):
                        print_d("This is the uploaded daltonized D-Image: " + d_uploaded_image_d.link + ", P-Image: " + d_uploaded_image_p.link + ", T-Image: " + d_uploaded_image_t.link)
                        print_d("This is the uploaded simulated D-Image: " + s_uploaded_image_d.link + ", P-Image: " + s_uploaded_image_p.link + ", T-Image: " + s_uploaded_image_t.link)
                        commentReply = "Here are your daltonized images:\n\nDeutan: " + d_uploaded_image_d.link + "\n\nProtan: " + d_uploaded_image_p.link + "\n\nTritan: " + d_uploaded_image_t.link + "\n\n&nbsp;\n\nHere are your simulated images:\n\nDeutan: " + s_uploaded_image_d.link + "\n\nProtan: " + s_uploaded_image_p.link + "\n\nTritan: " + s_uploaded_image_t.link + footer_text
                    else:
                        # The bot failed to upload the images to Imgur.
                        print_d("The Imgur links don't exist")
                        commentReply = "I'm sorry, but I was unable to upload the daltonized/simulated images to Imgur." + footer_text

                elif (daltonize_flag is True and simulate_flag is False):
                    if (d_uploaded_image_d is not None and d_uploaded_image_p is not None and d_uploaded_image_t is not None):
                        print_d("This is the uploaded daltonized D-Image: " + d_uploaded_image_d.link + ", P-Image: " + d_uploaded_image_p.link + ", T-Image: " + d_uploaded_image_t.link)
                        commentReply = "Here are your daltonized images:\n\nDeutan: " + d_uploaded_image_d.link + "\n\nProtan: " + d_uploaded_image_p.link + "\n\nTritan: " + d_uploaded_image_t.link + footer_text
                    else:
                        # The bot failed to upload the images to Imgur.
                        print_d("The Imgur links don't exist")
                        commentReply = "I'm sorry, but I was unable to upload the daltonized images to Imgur." + footer_text

                elif (daltonize_flag is False and simulate_flag is True):
                    if (s_uploaded_image_d is not None and s_uploaded_image_p is not None and s_uploaded_image_t is not None):
                        print_d("This is the uploaded simulated D-Image: " + s_uploaded_image_d.link + ", P-Image: " + s_uploaded_image_p.link + ", T-Image: " + s_uploaded_image_t.link)
                        commentReply = "Here your simulated images:\n\nDeutan: " + s_uploaded_image_d.link + "\n\nProtan: " + s_uploaded_image_p.link + "\n\nTritan: " + s_uploaded_image_t.link + footer_text
                    else:
                        # The bot failed to upload the images to Imgur.
                        print_d("The Imgur links don't exist")
                        commentReply = "I'm sorry, but I was unable to upload the simulated images to Imgur." + footer_text

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

sys.stdout = open("/dev/stdout", "w")
sys.stderr = open("/dev/stderr", "w")
