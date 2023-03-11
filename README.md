# dalton-bot

This repo is to create a bot for /r/colorblind, so the user's can request the bot to daltonize an image so it's viewable to those who have CVD, or to simulate what an image looks like for people with CVD

# Requirements
Docker

Docker Compose
  
# Installation
Clone the repo!   
`git clone https://gitlab.com/Haych/dalton-bot.git`  
Modify .env for the account details for your bot (Steps 1-3 from [here](https://www.instructables.com/Reddit-Reply-Bot/) will give you the details you need) and the Imgur API key.  
Make sure you have all of the requirements from above  

# How to run


First you need to build it. From inside the same directory as the dockerfile build the image using:

`docker build -t dalton-bot .`

Then run the container using:

`docker run -d --name dalton-bot dalton-bot:latest`

You can check the logs using

`docker logs -f dalton-bot`

If you want to stop the docker from running then run

`docker stop dalton-bot`

 
Special thanks to https://github.com/joergdietrich/daltonize for the daltonize.py script!  

If there is an error in the build such as `/simulated": not found` then run `mkdir simulated daltonized` and re-run the build.
