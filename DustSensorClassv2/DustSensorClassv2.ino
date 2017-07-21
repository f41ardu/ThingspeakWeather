/*
  Standalone Sketch to use with a Arduino Duemilanove, Uno, etc....  and a
  Sharp Optical Dust Sensor GP2Y1010AU0F
  06.11.2016 #thr  

Sharp pin 1 (V-LED)   => 5V (connected to 150ohm resister)
Sharp pin 2 (LED-GND) => Arduino GND pin
Sharp pin 3 (LED)     => Arduino pin 2
Sharp pin 4 (S-GND)   => Arduino GND pin
Sharp pin 5 (Vo)      => Arduino A5 pin
Sharp pin 6 (Vcc)     => 5V
*/
#include "GP2Y1010AU0F.h"

int measurePin = 5; //Connect dust sensor to Arduino A5 pin
int ledPower = 2;   //Connect D2 led driver pins of dust sensor to Arduino D2
double volt;
GP2Y1010AU0F DustSensor(ledPower, measurePin);

void setup() {
  Serial.begin(115200);
}

void loop() {
  
/*  Serial.print("Raw Signal Value (0-1023): ");
  Serial.print(,4);
  Serial.print(" - Voltage: ");
  Serial.print(GP2Y1010AU0F.voltage(),4);
  Serial.print(" - Dust Density: ");
*/
  if ( DustSensor.raw() > 0.0 ) 
  Serial.print(DustSensor.density(),4); // unit: mg/m3
  Serial.print(",");
  Serial.println(DustSensor.voltage(),4); // unit: Volt

  delay(1000);
}
