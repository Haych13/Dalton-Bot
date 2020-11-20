# r-Colorblind bot

This repo is to create a bot for /r/colorblind, so the user's can request the bot to daltonize an image so it's viewable to those who have CVD

# Requirements
python3  
pip  
pyimgur  
praw   
pillow  
Imgur API key - https://apidocs.imgur.com/  
  
# Installation
Clone the repo!   
`git clone https://gitlab.com/Haych/dalton-bot.git`  
Modify config.py for the account details for your bot (Steps 1-3 from [here](https://www.instructables.com/Reddit-Reply-Bot/) will give you the details you need) and the Imgur API key.  
Make sure you have all of the requirements from above  

# How to run

You can run the bot in the background using nohup, this will leave a log in a new file called output.log  
  
`nohup python3 -u dalton_bot.py >> output.log &`  

If you need to kill the bot search for the PID then kill  
  
`ps -ef | grep dalton_bot.py`  
  
`kill -PID from above-`  
  
  
    
      
  
Special thanks to https://github.com/joergdietrich/daltonize for the daltonize.py script!  