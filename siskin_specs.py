birdname = "siskin"
VIDEO_PATH = Path("trron_" + birdname + "_final.mp4")
player = OMXPlayer(VIDEO_PATH, args=['--no-osd', '--no-keys', '-b'])

''' The following variables need to be changed from one
    program to the next. They are the times when each event happens
    in the videos.'''
flyin = 2 #when the bird flies onto the feeder, minus a couple of seconds
feeding = 6 #when the bird begins feeding, for looping back to the feeding sequence
flyaway = 137 #the point where the bird flies away
empty = 143 #where there is an empty section so the empty feeder can be looped back to this point
player_length = 165 #the total length of the video, minus three to avoid missing the sleep timer and overrunning the video
