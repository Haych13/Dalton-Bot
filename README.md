# dalton-bot

This repo is to create a bot for /r/colorblind, so the user's can request the bot to daltonize an image so it's viewable to those who have CVD, or to simulate what an image looks like for people with CVD

# Requirements
Docker/ Docker Compose
  
Before running, you will need reddit acccount details for your bot (Steps 1-3 from [here](https://www.instructables.com/Reddit-Reply-Bot/) will give you the details you need) and an Imgur API key.  

There are a few variables that need changing prior to running

```
USERNAME
PASSWORD
CLIENT_ID
CLIENT_SECRET
IMGUR_CLIENT_ID
FOOTER_TEXT
D_OUTPUT_DIR_DEUTERANOPIA
D_OUTPUT_DIR_PROTANOPIA
D_OUTPUT_DIR_TRITANOPIA
S_OUTPUT_DIR_DEUTERANOPIA
S_OUTPUT_DIR_PROTANOPIA
S_OUTPUT_DIR_TRITANOPIA
```

# Docker 

```
docker run \
-e USERNAME=username \
-e PASSWORD=password \
-e CLIENT_ID=client-id \
-e CLIENT_SECRET=client-secret \
-e IMGUR_CLIENT_ID=imgur_id \
-e FOOTER_TEXT=footer-text \
-e D_OUTPUT_DIR_DEUTERANOPIA=daltonized/deuteranopia.jpg \
-e D_OUTPUT_DIR_PROTANOPIA=daltonized/protanopia.jpg \
-e D_OUTPUT_DIR_TRITANOPIA=daltonized/tritanopia.jpg \
-e S_OUTPUT_DIR_DEUTERANOPIA=simulated/deuteranopia.jpg \
-e S_OUTPUT_DIR_PROTANOPIA=simulated/protanopia.jpg \
-e S_OUTPUT_DIR_TRITANOPIA=simulated/tritanopia.jpg \
dalton-bot:latest
```
# Docker-compose
```
services:
  dalton-bot:
    image: haych13/dalton-bot:latest
    container_name: dalton-bot
    environment:
      - USERNAME=username
      - PASSWORD=password
      - CLIENT_ID=client-id
      - CLIENT_SECRET=client-secret
      - IMGUR_CLIENT_ID=imgur_id
      - FOOTER_TEXT=footer-text
      - D_OUTPUT_DIR_DEUTERANOPIA=daltonized/deuteranopia.jpg
      - D_OUTPUT_DIR_PROTANOPIA=daltonized/protanopia.jpg
      - D_OUTPUT_DIR_TRITANOPIA=daltonized/tritanopia.jpg
      - S_OUTPUT_DIR_DEUTERANOPIA=simulated/deuteranopia.jpg
      - S_OUTPUT_DIR_PROTANOPIA=simulated/protanopia.jpg
      - S_OUTPUT_DIR_TRITANOPIA=simulated/tritanopia.jpg
    restart: unless-stopped
```

Alternatively, you can use an .env file and modify that

```
  dalton-bot:
    image: haych13/dalton-bot:latest
    container_name: dalton-bot
    env_file:
      - ./dalton-bot/.env 
        
    restart: unless-stopped
```


.env contents:
```
USERNAME="Bot-Name"
PASSWORD="Bot-Password"
CLIENT_ID="Bot-ID"
CLIENT_SECRET="Bot-Secret"
IMGUR_CLIENT_ID="imgurclientid"
FOOTER_TEXT="\n\n---\n\n^^*I* ^^*am* ^^*a* ^^*bot,* ^^*and* ^^*this* ^^*action* ^^*was* ^^*performed* ^^*automatically.* &#32;  \n^^[What-am-I?](https://www.reddit.com/r/DaltonBot/wiki/index)&#32; ^^| ^^[Subreddit](http://www.reddit.com/r/DaltonBot/)&#32; ^^| ^^[Source](https://gitlab.com/Haych/dalton-bot)"
D_OUTPUT_DIR_DEUTERANOPIA="daltonized/deuteranopia.jpg"
D_OUTPUT_DIR_PROTANOPIA="daltonized/protanopia.jpg"
D_OUTPUT_DIR_TRITANOPIA="daltonized/tritanopia.jpg"
S_OUTPUT_DIR_DEUTERANOPIA="simulated/deuteranopia.jpg"
S_OUTPUT_DIR_PROTANOPIA="simulated/protanopia.jpg"
S_OUTPUT_DIR_TRITANOPIA="simulated/tritanopia.jpg"
```

https://hub.docker.com/r/haych13/dalton-bot
