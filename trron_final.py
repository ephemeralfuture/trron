from omxplayer.player import OMXPlayer #runs from the popcornmix omxplayer wrapper at https://github.com/popcornmix/omxplayerhttps://github.com/popcornmix/omxplayer and https://python-omxplayer-wrapper.readthedocs.io/en/latest/)
from pathlib import Path
import time
#import sys, tty, termios
#from msvcrt import getch
import RPi.GPIO as GPIO #for taking signal from GPIO
#import subprocess
#import logging
#logging.basicConfig(level=logging.INFO)

import os
import sys
buf_arg = 0
if sys.version_info[0] == 3:
    os.environ['PYTHONUNBUFFERED'] = '1'
    buf_arg = 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_PIR = 7

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo
 
Current_Motion  = 0 #the current state of motion detection
Previous_Motion = 0 #the previous state

VIDEO_PATH = Path("siskin_full_chaptertest.m4v")
#player_log = logging.getLogger("Player 1")

player = OMXPlayer(VIDEO_PATH)
#dbus = 'org.mpris.MediaPlayer2.omxplayer1'
#player.playEvent += lambda _: player_log.info("Play")
#player.pauseEvent += lambda _: player_log.info("Pause")
#player.stopEvent += lambda _: player_log.info("Stop")

flyin = 4
feeding = 9
flyaway = 40
empty = 44

current_mode = 0 #determines which mode the player is in

motion_detect_bool = False



def flyin_mode():
    player.set_position(flyin)
    print("player seeked to " + str(player.position()) + "for flyin")

def feeding_mode():
    player.set_position(feeding)
    print("player seeked to " + str(player.position()) + "for feeding")

def flyaway_mode():
    player.set_position(flyaway)
    print("player seeked to " + str(player.position()) + "for flyaway")

def empty_mode():
    player.set_position(empty)
    print("player seeked to " + str(player.position()) + "for empty")


def check_motion_sensor(Current_Motion, Previous_Motion):
    Current_Motion = GPIO.input(GPIO_PIR) # Read PIR state
    print("checked current motion and it is " + str(Current_Motion))
    print("checked previous motion and it is " + str(Previous_Motion))
    time.sleep(1)
    if Current_Motion == 1 and Previous_Motion == 0:
        Previous_Motion = 1
        return True
    elif Current_Motion == 0 and Previous_Motion == 1:
        Previous_Motion = 0
        return False



try:
    
    print ("Waiting for PIR to settle ...")
    print(GPIO.input(GPIO_PIR))
 
    print ("  Ready")
    
    player.play()
    
    
        
    
    
    while True:
                
        if current_mode == 0:
            player.play()
            time.sleep(1)
            current_mode = 1
    
        if current_mode == 1:
            flyin_mode()
            time.sleep(1)
            current_mode = 2
        
        if current_mode == 2:
            motion_detect_bool = check_motion_sensor(Current_Motion, Previous_Motion)
            if motion_detect_bool == True:
                current_mode = 3
            elif motion_detect_bool == False:
                if player.position() > flyaway-2: #loops the feeding mode before flyaway happens
                    feeding_mode()
                    time.sleep(1)
                
        
        if current_mode == 3:
            flyaway_mode()
            time.sleep(2)
            current_mode = 4
        
        if current_mode == 4:
            motion_detect_bool = check_motion_sensor(Current_Motion, Previous_Motion)
            if motion_detect_bool == True:
                print("still motioned!")
                if int(player.position()) > empty+5:
                    empty_mode()
                    time.sleep(3)
            elif motion_detect_bool == False:
                print("no more motion!")
                current_mode = 1


        # Wait for 10 milliseconds
        time.sleep(1)
        print("current mode is " + str(current_mode))
        print("current player time is " + str(player.position()))
        print(int(player.position()))
        print(motion_detect_bool)

except KeyboardInterrupt:
  print ("  Quit")
  # Reset GPIO settings
  GPIO.cleanup()