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
empty = 195 #where there is an empty section so the empty feeder can be looped back to this point

current_mode = 0 #determines which mode the player is in

motion_detect_bool = False #boolean for detecting motion

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
    time.sleep(1)
    if Current_Motion == 1 and Previous_Motion == 0:
        Previous_Motion = 1
        return True
    elif Current_Motion == 0 and Previous_Motion == 1:
        Previous_Motion = 0
        return False

try:
    player.play()
    
    while GPIO.input(GPIO_PIR) == 1: #loop while the motion sensor is setting up and still reading high
        print ("Waiting for PIR to settle ...")
        time.sleep(2)
 
    print ("  Ready")
    
    current_time = int(time.time())

    while True:
        
        motion_sonsor_reading = GPIO.input(GPIO_PIR)
        
        if current_mode == 0:
            player.play()
            next_mode = 1
    
        if current_mode == 1:
            flyin_mode()
            next_mode = 2
        
        if current_mode == 2:
            motion_detect_bool = check_motion_sensor(Current_Motion, Previous_Motion)
            if motion_detect_bool == True:
                next_mode = 3
            elif motion_detect_bool == False:
                if player.position() > flyaway-2: #loops the feeding mode before flyaway happens
                    feeding_mode()                
        
        if current_mode == 3:
            flyaway_mode()
            next_mode = 4
        
        if current_mode == 4:
            motion_detect_bool = check_motion_sensor(Current_Motion, Previous_Motion)
            if motion_detect_bool == True:
                print("still motioned!")
                if int(player.position()) > empty+5:
                    empty_mode()
            elif motion_detect_bool == False:
                print("no more motion!")
                next_mode = 1

        if next_mode is not None:
            current_mode = next_mode #changes mode
        
        time.sleep(5) #sleep for 5 seconds
        print("current mode is " + str(current_mode))
        print("motion detect reading is " + str(motion_sonsor_reading))
        print("current time is " + str(current_time))

except KeyboardInterrupt:
    print ("  Quit")
    # Reset GPIO settings
    GPIO.cleanup()