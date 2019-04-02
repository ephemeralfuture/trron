#include "Ultrasonic.h"

int TRIG = 2; // Trigger Pin
int ECHO = 3; // Echo Pin
int Range; // The range of the object from the HC-SR04 Ultarsonic Module
 
Ultrasonic ultrasonic(TRIG,ECHO); // Create and initialize the Ultrasonic object.


void setup()
{
  Serial.begin(9600);
}

void loop() {
 
  Range = ultrasonic.Ranging(CM); // Range is calculated in Centimeters.
  // Range = ultrasonic.Ranging(INC); // Range is calculated in Inches.
 

int val = map(analogRead(Range), 0, 1023, 0, 255);
 
  Serial.print(Range);  
  Serial.println("CM");
  Serial.println(val);
  delay(50);
 
}
