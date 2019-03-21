import processing.video.*;

Movie test_movie; //movie (any test movie)
Movie test_movie_empty;
Movie test_movie_feed;
Movie test_movie_flyaway;
boolean jumpy = false; //boolean controller so the keypressed doesn't constantly run

void setup(){
  frameRate(30); //base framerate for PAL, should also speed up video playback
  test_movie_empty = new Movie (this, "birds_test1_empty.mp4"); //name of movie to be set
  test_movie_feed = new Movie (this, "birds_test1_feed.mp4"); //name of movie to be set
  test_movie_flyaway = new Movie (this, "birds_test1_flyaway.mp4"); //name of movie to be set
  fullScreen(); //run in fullscreen
  noSmooth(); //improve framerate by removing image smoothing
  //noLoop(); //not sure if necessary, for improving 
  test_movie = test_movie_feed;
  test_movie.loop(); //play movie
  test_movie_flyaway.loop();

}

void draw(){
  if (keyPressed && jumpy == false){ //run once - boolean ensures it doesn't keep running
    jumpy = true; //set boolean
  }
  if(jumpy == false){
    image(test_movie, 0, 0); //show movie as image
  }else{
    image(test_movie_flyaway, 0, 0); //show movie as image
  }
  
}

void movieEvent(Movie test_movie) { //to read the movie data
    test_movie.read();
}
