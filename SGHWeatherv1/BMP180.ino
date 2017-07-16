struct pressureValues _bmp180() {
  char status;
  //double T, P, p0, a;
  struct pressureValues bmp180;

  // If you want to measure altitude, and not pressure, you will instead need
  // to provide a known baseline pressure. This is shown at the end of the sketch.

  // You must first get a temperature measurement to perform a pressure reading.

  // Start a temperature measurement:
  // If request is successful, the number of ms to wait is returned.
  // If request is unsuccessful, 0 is returned.

  status = pressure.startTemperature();
  if (status != 0)
  {
    // Wait for the measurement to complete:
    delay(status);

    // Retrieve the completed temperature measurement:
    // Note that the measurement is stored in the variable T.
    // Function returns 1 if successful, 0 if failure.

    status = pressure.getTemperature(bmp180.T);
    if (status != 0)
    {
      // Print out the measurement:
      //Serial.print("temperature: ");

      /* Serial.print((9.0/5.0)*T+32.0,2);
        Serial.print(" "); */

      // Start a pressure measurement:
      // The parameter is the oversampling setting, from 0 to 3 (highest res, longest wait).
      // If request is successful, the number of ms to wait is returned.
      // If request is unsuccessful, 0 is returned.

      status = pressure.startPressure(3);
      if (status != 0)
      {
        // Wait for the measurement to complete:
        delay(status);

        // Retrieve the completed pressure measurement:
        // Note that the measurement is stored in the variable P.
        // Note also that the function requires the previous temperature measurement (T).
        // (If temperature is stable, you can do one temperature measurement for a number of pressure measurements.)
        // Function returns 1 if successful, 0 if failure.

        status = pressure.getPressure(bmp180.P, bmp180.T);
        if (status != 0)
        {
        

          // The pressure sensor returns abolute pressure, which varies with altitude.
          // To remove the effects of altitude, use the sealevel function and your current altitude.
          // This number is commonly used in weather reports.
          // Parameters: P = absolute pressure in mb, ALTITUDE = current altitude in m.
          // Result: p0 = sea-level compensated pressure in mb
          
          bmp180.p0 = pressure.sealevel(bmp180.P, ALTITUDE); // we're at 1655 meters (Boulder, CO)
        
          // On the other hand, if you want to determine your altitude from the pressure reading,
          // use the altitude function along with a baseline pressure (sea-level or other).
          // Parameters: P = absolute pressure in mb, p0 = baseline pressure in mb.
          // Result: a = altitude in m.

          bmp180.a = pressure.altitude(bmp180.P, bmp180.p0);
         
        }
        else //Serial.println("error retrieving pressure measurement\n");+
          pseudo = 0;
      }
      else //Serial.println("error starting pressure measurement\n");
        pseudo = 0;
    }
    else //Serial.println("error retrieving temperature measurement\n");
      pseudo = 0;
  }
  else //Serial.println("error starting temperature measurement\n");
    pseudo = 0;
  return (bmp180);
}
