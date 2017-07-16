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

  Hardware connections:

  - (GND) to GND
  + (VDD) to 3.3V

  (WARNING: do not connect + to 5V or the sensor will be damaged!)

  You will also need to connect the I2C pins (SCL and SDA) to your
  Arduino. The pins are different on different Arduinos:

  Any Arduino pins labeled:  SDA  SCL
  Uno, Redboard, Pro:        A4   A5
  Mega2560, Due:             20   21
  Leonardo:                   2    3

  Leave the IO (VDDIO) pin unconnected. This pin is for connecting
  the BMP180 to systems with lower logic levels such as 1.8V

*/
#include "GP2Y1010AU0F.h"
#include <SFE_BMP180.h>
#include <Wire.h>

int measurePin = 5; //Connect dust sensor to Arduino A5 pin
int ledPower = 2;   //Connect D2 led driver pins of dust sensor to Arduino D2
double volt;

GP2Y1010AU0F DustSensor(ledPower, measurePin);

SFE_BMP180 pressure;

//double baseline; // baseline pressure

#define ALTITUDE 485.590 // Altitude of SparkFun's HQ in Boulder, CO. in meters
int pseudo;

struct pressureValues {
  double T;
  double P;
  double p0;
  double a;
} pressureValue;


void setup() {
  Serial.begin(9600);
  pressure.begin();
}

void loop() {

//  char status;
//  double T, P, p0, a;
  struct pressureValues Messung;

  Messung = _bmp180();
  if ( DustSensor.raw() >= 0.0 )  {
    Serial.print(Messung.p0);
    Serial.print(",");
    Serial.print(Messung.P);
    Serial.print(",");
    Serial.print(Messung.T);
    Serial.print(100.0 * DustSensor.density(), 4); // unit: mg/m3
    Serial.print(",");
    Serial.println(DustSensor.voltage(), 4); // unit: Volt
  }
  delay(1000);
}
