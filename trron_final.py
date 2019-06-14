from omxplayer.player import OMXPlayer #runs from the popcornmix omxplayer wrapper at https://github.com/popcornmix/omxplayerhttps://github.com/popcornmix/omxplayer and https://python-omxplayer-wrapper.readthedocs.io/en/latest/)
from pathlib import Path
import time
#import sys, tty, termios
#from msvcrt import getch
import RPi.GPIO as GPIO #for taking signal from GPIO
import subprocess
import logging
logging.basicConfig(level=logging.INFO)


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

positionEvent = 12
flyin = 3
feeding = 6
flyaway = 25
empty = 38

current_mode = 0 #determines which mode the player is in

motion_detect_bool = False

currtime = int(player.position())

#time.sleep(60) #need to sleep at the beginning to allow the PIR t initialise

def checktime():
    currtime = int(player.position())
    #print("current time is " + str(currtime))

def flyin_mode():
    checktime()
    player.seek(flyin-currtime)
    print("player seeked to " + str(player.position()) + "for flyin")

def feeding_mode():
    checktme()
    player.seek(feeding-currtime)
    print("player seeked to " + str(player.position()) + "for feeding")

def flyaway_mode():
    checktime()
    player.seek(flyaway-currtime)
    print("player seeked to " + str(player.position()) + "for flyaway")

def empty_mode():
    checktime()
    player.seek(empty-currtime)


def check_motion_sensor():
    Current_Motion = GPIO.input(GPIO_PIR) # Read PIR state
    time.sleep(1)
    if Current_Motion == 1 and Previous_Motion == 0:
        return True
    elif Current_Motion == 0 and Previous_Motion == 1:
        return False



try:
    
    print ("Waiting for PIR to settle ...")
    print(GPIO.input(GPIO_PIR))
 
    print ("  Ready")
    
    
        
    
    
    while True:
        
        player.play()
        
        if current_mode == 0:
            player.play()
            current_mode = 1
    
        if current_mode == 1:
            flyin_mode()
            time.sleep(1)
            current_mode = 2
        
        if current_mode == 2:
            checktime()
            motion_detect_bool = check_motion_sensor()
            if motion_detect_bool == True:
                current_mode = 3
            elif motion_detect_bool == False:
                if currtime > flyaway-2: #loops the feeding mode before flyaway happens
                    feeding_mode()
                    time.sleep(1)
                
        
        if current_mode == 3:
            flyaway_mode()
            time.sleep(2)
            current_mode = 4
        
        if current_mode == 4:
            motion_detect_bool = check_motion_sensor()
            checktime()
            if motion_detect_bool == True:
                print("still motioned!")
                if currtime > empty+5:
                    empty_mode()
                    time.sleep(3)
            elif motion_detect_bool == False:
                print("no more motion!")
                current_mode = 1


        # Wait for 10 milliseconds
        time.sleep(1)
        print("current mode is " + str(current_mode))
        print("current player time is " + str(player.position()))
        print("current currtime is " + str(currtime))

except KeyboardInterrupt:
  print ("  Quit")
  # Reset GPIO settings
  GPIO.cleanup()