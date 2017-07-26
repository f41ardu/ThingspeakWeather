# -*- coding: utf-8 -*-

#
# "THE WHISKEY-WARE LICENSE" (Revision ln(e))
# <tom@hash-n-bush.de> schrieb diese Datei. Solange Sie diesen Vermerk
# nicht entfernen, können Sie mit diesem Phyton Code machen was Sie wollen.
# Dieser Quelltext ist frei, so wie "frei" in "Die Gedanken sind frei". 
# Sollten wir uns eines Tages treffen und Sie denken, das ist es wert, dann
# geben Sie mir einen Whisky aus. tom.#-n-bush
#
#

# --- thr 2017-07-16 physical::computing AG SGH / Holzgerlingen 
# for Phyton 3.x 
# v 1.0
# Lesen und schreiben von mehren Datenfeldern
# 
# 
# updateThingspeakv3.py
# 
# dependency: a library file containing the thingspeak api keys 
# 'thingspeak_keys.py' containing eg:
# RASPBERRY_PI2  = "KEYABCXYZETECETC"
# a library thingspeak.v3 as API to thingspeak.com  


import serial
import time
import ast

# =======================
# import my local modules
import thingspeak_keys
import thingspeak3

# thingspeak api key & data dictionary
TS_KEY              = thingspeak_keys.RASPBERRY_PI2
thingspeak_data     = {}

# =======================
# some definitions
PORT = '/dev/ttyUSB0'
BAUD =  115200
TIMEOUT = 0.5
# =======================
# open serial communication 
serialPort = serial.Serial(PORT,BAUD)

# =====================
# function readsensors 
def readSensors(port):
    # =====================
    # read from serial port 
    if port.inWaiting()>0:
           try: 
               rcv = port.readline().decode().replace('\n', '').replace('\r', '')
           except(ValueError):
               print("Redline Error")
           return rcv.split(',')
        
# =============================
# ignore the first 100 readings
i = 100
while i>1:
      values = readSensors(serialPort)      
      print(values)
      i=i-1
# =======================      
# start update thingspeak 
while True:
        # =================================================
        # read sensors
        values = readSensors(serialPort)
        if values:
           try:
               # ==========================================   
               # convert to float
               dust=ast.literal_eval(values[0])
               voltage=ast.literal_eval(values[1])
               # ==========================================
               # populate the thingspeak content dictionary
               thingspeak_data['field1'] = dust
               thingspeak_data['field2'] = voltage
               print((dust, voltage))
               # ==========================================
               # update thingspeak 
               thingspeak3.post(TS_KEY, thingspeak_data)
           # ==============================================
           # no data from sensor
           except:
               print('Sensor Read Error')
        # =================================================
        # wait 20 seconds
        time.sleep(20)
