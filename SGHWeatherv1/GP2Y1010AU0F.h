// http://de.wikibooks.org/wiki/C%2B%2B-Programmierung:_Klassen

#ifndef GP2Y1010AU0F_H
#define GP2Y1010AU0F_H

#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"  // for digitalRead, digitalWrite, etc
#else
#include "WProgram.h"
#endif
//#include <Arduino.h> //It is very important to remember this! note that if you are using Arduino 1.0 IDE, change "WProgram.h" to "Arduino.h"

#define samplingTime 280
#define deltaTime 40
#define sleepTime 9680

class GP2Y1010AU0F
{
  public:                             // öffentlich
    GP2Y1010AU0F();                     // der Default-Konstruktor
    GP2Y1010AU0F(int, int);             // weiterer Konstruktor mit Parameter
    //   PinClass(const LED& a);      // Copy-Konstruktor wird nicht benötigt
    ~GP2Y1010AU0F();                    // Class Destruktor

    double density();              // Staubdichte ausgeben µg/m^3
    double raw();                      // raw daten ausgeben
    double voltage();                  // spannung berechnen

  private:                            // privat
    int _ledPin, _measurePin;

    double voMeasured = 0;
    double calcVoltage = 0;
    double calDensity = 0;
    double _calcVoltage = 0; 
    double _calDensity = 0; 

};

#endif // GP2Y1010AU0F_H

