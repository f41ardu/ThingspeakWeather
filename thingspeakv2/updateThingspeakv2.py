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
# for Phyton 2.7 
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

import numpy as np
from matplotlib import pyplot as plt

# Tutorial
# See http://www.labri.fr/perso/nrougier/teaching/matplotlib/ 

# =======================
# import my local modules
import thingspeak_keys
import thingspeak

# thingspeak api key & data dictionary
TS_KEY              = thingspeak_keys.RASPBERRY_PI2
thingspeak_data     = {}

# =======================
# some definitions
PORT = '/dev/ttyUSB0'
BAUD =  115200
TIMEOUT = 0.5

plt.ion() # set plot to animated
 
ydata = [0] * 50
ydata1 = [0] * 50
ax1=plt.axes() 
 
# make plot
line, = plt.plot(ydata)
line1,= plt.plot(ydata1)
plt.ylim([0,10])

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
#      print(values)
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
               thingspeak.post(TS_KEY, thingspeak_data)
               # plot data
               data=dust
               data1=voltage*5
               ymin = 0. #float(min(ydata))#-10
               ymax = float(max(ydata))+2
               plt.ylim([ymin,ymax])
               ydata.append(data)
               ydata1.append(data1)
               del ydata[0]
               del ydata1[0]
               line.set_xdata(np.arange(len(ydata)))
               line.set_ydata(ydata)  # update the data
               line1.set_ydata(ydata1)  # update the data
               plt.grid(True)
               plt.draw() # update the plot
           # ==============================================
           # no data from sensor
           except:
               print('Sensor Read Error')
        # =================================================
        # wait 20 seconds
        time.sleep(20)
