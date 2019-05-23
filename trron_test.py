from omxplayer.player import OMXPlayer #runs from the popcornmix omxplayer wrapper at https://github.com/popcornmix/omxplayerhttps://github.com/popcornmix/omxplayer and https://python-omxplayer-wrapper.readthedocs.io/en/latest/)
from pathlib import Path
import time
#import sys, tty, termios
#from msvcrt import getch
import RPi.GPIO as GPIO #for taking signal from GPIO
import subprocess


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27,GPIO.OUT)

GPIO_PIR = 7

VIDEO_PATH = Path("siskin_full.mp4")

player = OMXPlayer(VIDEO_PATH)
positionEvent = 3

while True:
    key = input()
    
    currtime = player.position()
    
    if(currtime > 3):
        player.seek(-300)
        print(currtime)

    if key == 'h':
        player.seek(300)
        
#player.loop()

sleep(5)

#player.quit()