/*The following program is a test for the layered images program written for
an artwork to be displayed at the Zoology Museum, Trinity College Dublin,
June 2019. The artwork uses layered videos to display different states 
based on a person's proximity to a distance sensor, read from an Arduino program,
'distance_sensor.ino'. When a person is nearby, the birds fly 
away. Written by Shane Finan with collaboration from Gary McDermott, 
Feb-May 2019. Supported by Trinity College Dublin Visual and 
Performing Arts Fund*/

import processing.video.*; //imports video library for video processing
import processing.serial.*; //imports serial to read from Arduino

String birdname = "siskin";  //the video files are named after 
                            //each bird. This is called when 
                            //these files are loaded in setup()
/* Four movie files are loaded for the four states of each 
piece. Descriptions below. */

Movie no_bird; //the bird feeder without bird
Movie flyin; //the video where the bird flies into shot
Movie feeding; //the video of the bird feeding
Movie flyaway; //the video of the bird flying away

Boolean still_there = false; //a boolean to check if user is still 
                      //standing near sensor
Boolean startled = false; //a boolean to check if the user has triggered the sensor
int flyaway_length; //length in miliseconds of the 'flyaway' movie, called in setup
int flyin_length; //as above, for the flyin movie
int startled_begin; //a variable for recognising when the sensor is first triggered
int startled_end; //ditto as above, for the reverse state

void setup(){
  frameRate(30); //base framerate for PAL, should also speed up video playback
  //below load videos using 'birdname' variable
  no_bird = new Movie (this, birdname + "_empty.mp4");
  flyin = new Movie (this, birdname + "_fly_in.mp4");
  feeding = new Movie (this, birdname + "_feeding.mp4");
  flyaway = new Movie (this, birdname + "_flyaway.mp4");
  
  //NOT WORKING flyaway_length = int(flyaway.duration()*1000); //reads duration of flyaway video and multiplies for miliseconds
  flyaway_length = 3500;
  flyin_length = 14000;
  
  fullScreen(); //run in fullscreen
  noSmooth(); //improve framerate by removing image smoothing
  //loop all movie files
  no_bird.loop();
  feeding.loop();
}

void draw(){
  
  Boolean active = check_state(); // a function to check the current state (flexible so can be replaced with testing and with Serial reads)
  
  if (startled == false){
    if (still_there == false){ //checking if user has stayed near the machine
      image(feeding, 0, 0);
    }
    if (still_there == true && startled_end+flyin_length>millis()){
      flyin.play();
      image(flyin, 0, 0);
    }
    if(startled_end+flyin_length<millis()){
      still_there = false; //reverts so the feeding loop now plays
    }
  }
  if(active == true && startled == false){ //testing with keyPressed() to be replaced by Arduino serial read
    startled = true; //set boolean
    flyaway.play(); //play flyway video (limited time, see below)
    startled_begin = millis(); //timer to set when the 'flyaway' movie ends
  }
  if (startled == true && startled_begin+flyaway_length>millis()){
    image(flyaway, 0, 0); //show flyaway video
  }
  if (startled == true && startled_begin+flyaway_length<millis()){
    image(no_bird, 0, 0); //show nobird video on loop until boolean is reset
  }
  if(active==false && startled == true && startled_begin+flyaway_length<millis()){
    startled = false; //reset startled variable
    still_there = true; //user is no longer by the machine
    startled_end = millis();
  }
  text("flyaway_length: " + flyaway_length, 50, 50);
}

void movieEvent(Movie test_movie) { //to read the movie data
    test_movie.read();
}

Boolean check_state(){
  //to be written to take in read from Serial, currently working off keypressed()
  if (keyPressed){
    return true;
  }else{
    return false;
  }
}
