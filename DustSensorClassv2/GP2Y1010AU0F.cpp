#include "GP2Y1010AU0F.h"

GP2Y1010AU0F::GP2Y1010AU0F():
  _ledPin(0), _measurePin(0)
{
  // Default Constructor
}

GP2Y1010AU0F::GP2Y1010AU0F(int ledPin, int measurePin):
  _ledPin(ledPin), _measurePin(measurePin)
  // SensorPin initialisieren
{
  pinMode(_ledPin, OUTPUT);
}

// Destructor
GP2Y1010AU0F::~GP2Y1010AU0F()
// Destructore
{

}
double GP2Y1010AU0F::raw()
{
  // Sensor auslesen
  digitalWrite(_ledPin, LOW); // power on the LED
  delayMicroseconds(samplingTime);
  voMeasured = analogRead(_measurePin); // read the dust value
  delayMicroseconds(deltaTime);
  digitalWrite(_ledPin, HIGH); // turn the LED off
  delayMicroseconds(sleepTime);
  _calcVoltage = voMeasured * (5.0 / 1024.0);
// linear eqaution taken from http://www.howmuchsnow.com/arduino/airquality/
// Chris Nafis (c) 2012
  _calDensity = 0.172 * _calcVoltage - 0.0999;
 //  _calDensity = 0.17 * _calcVoltage - 0.1;
  return voMeasured;
  
}

double GP2Y1010AU0F::voltage()
{  
  return _calcVoltage;
}

double GP2Y1010AU0F::density()
{
  if (_calDensity <= 0.0) {
    return 0.0;
  } else {
    return _calDensity;
  }
}



