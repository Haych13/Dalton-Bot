mkdir -p /opt/DaltonBot && cp -f config.py  dalton_bot.py  Dalton-bot.service  daltonize.py  LICENSE  README.md /opt/DaltonBot/

if [ -d /usr/lib/systemd/system/ ] ; then cp -f Dalton-bot.service /usr/lib/systemd/system/
        
else echo " Use systemctl enable $0 and systemctl start $0 to begin"  
echo " $0 creation fail: Likely a system without systemd"             
        
fi