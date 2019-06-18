'''
This program is written by visual artist Shane Finan (www.shanefinanart.org)
to control a multi-display video piece on Raspberry Pis.
The artwork loops videos of birds feeding until a
motion sensor is triggered, which jumps the videos to the point
when the birds fly away. All videos are triggered off the same PIR
motion sensor, hooked into a GPIO on each Raspberry Pi.

The artwork is staged in the Zoological Museum, Trinity College
Dublin in June ad July 2019.

The program uses Will Price's omxplayer-wrapper: https://github.com/willprice/python-omxplayer-wrapper
Some help on testing and development of PIR sensor reading and motion was taken from: https://www.raspberrypi-spy.co.uk/2013/01/cheap-pir-sensors-and-the-raspberry-pi-part-1/
Many thanks to contributions on the Raspberry Pi forum for help in development.
'''

from omxplayer.player import OMXPlayer #runs from the popcornmix omxplayer wrapper at https://github.com/popcornmix/omxplayerhttps://github.com/popcornmix/omxplayer and https://python-omxplayer-wrapper.readthedocs.io/en/latest/)
from pathlib import Path
import time #for determining the time of playback
import RPi.GPIO as GPIO #for taking signal from GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_PIR = 7 #The GPIO is plugged into BCM pin 07 (GPIO pin 26)
GPIO.setup(GPIO_PIR,GPIO.IN) # Set pin as input
 
Current_Motion  = 0 #the current state of motion detection
Previous_Motion = 0 #the previous state

birdname = "goldfinch"
VIDEO_PATH = Path("trron_" + birdname + "_final.mp4")

player = OMXPlayer(VIDEO_PATH)


''' The following variables need to be changed from one
    program to the next. They are the times when each event happens
    in the videos.'''
flyin = 2 #when the bird flies onto the feeder, minus a couple of seconds
feeding = 6 #when the bird begins feeding, for looping back to the feeding sequence
flyaway = 192 #the point where the bird flies away
empty = 197 #where there is an empty section so the empty feeder can be looped back to this point
player_length = 218 #the total length of the video, minus three to avoid missing the sleep timer and overrunning the video

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

try:
    if player.is_playing() == False:
        player.play()
    
    while GPIO.input(GPIO_PIR) == 1: #loop while the motion sensor is setting up and still reading high
        print ("Waiting for PIR to settle ...")
        time.sleep(2)
 
    print ("  Ready")
    
    while True:
        
        if int(player.position()) > player_length: #check once for error here, in case the cue is missed and this overruns the player length
            empty_mode()
        
        motion_sensor_reading = GPIO.input(GPIO_PIR)
        print("motion detect reading is " + str(motion_sensor_reading))
        checktime = time.time() #three second check below for any change in motion sensor reading while it is on cooldown
        while motion_sensor_reading == 0 and time.time() < checktime + 3:
            motion_sensor_reading = GPIO.input(GPIO_PIR)
            print("seond check on motion sensor is " + str(motion_sensor_reading))
            if motion_sensor_reading ==1:
                break
        
        if motion_sensor_reading == 1:
            if int(player.position()) < flyaway and int(player.position()) > feeding:
                flyaway_mode()
                time.sleep(player_length-empty) #sleep until video runs out, once
                empty_mode()
            elif int(player.position()) > empty and int(player.position()) > player_length:
                empty_mode()
                time.sleep(player_length-empty) #sleep until video runs out, once
                
        elif motion_sensor_reading == 0:
            if motion_sensor_reading == 0: #checks again, after above while loop
                if int(player.position()) > flyaway:
                    motion_sensor_reading = GPIO.input(GPIO_PIR) #check motion sensor again, in case it has been triggered in the interim during the 3-seoncd interval
                    if motion_sensor_reading == 1 and int(player.position()) > empty and int(player.position()) > player_length:
                        empty_mode()
                    elif motion_sensor_reading == 0:    
                        flyin_mode()
                elif int(player.position()) < flyaway and int(player.position()) > flyaway-4:
                    feeding_mode()
        
except KeyboardInterrupt:
    print ("  Quit")
    # Reset GPIO settings
    GPIO.cleanup()