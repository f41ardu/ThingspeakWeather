# -*- coding: utf-8 -*-
# this is the library file that is imported by another python script
# depends upon the python library
# 'httplib' https://pypi.python.org/pypi/httplib2/0.9.1
# and
# 'urllib' https://docs.python.org/2/library/urllib.html

# "THE WHISKEY-WARE LICENSE" (Revision ln(e))
# <tom@hash-n-bush.de> schrieb diese Datei. Solange Sie diesen Vermerk
# nicht entfernen, können Sie mit diesem Phyton Code machen was Sie wollen.
# Dieser Quelltext ist frei, so wie "frei" in "Die Gedanken sind frei". 
# Sollten wir uns eines Tages treffen und Sie denken, das ist es wert, dann
# geben Sie mir einen Whisky aus. tom.#-n-bush
#

#
# thr --- 2017-07-22
#
# version 1.1

import os
import serial
import ast
import time
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#=======================
# import my local modules
import thingspeak_keys
import thingspeak

# thingspeak api key & data dictionary
TS_KEY              = thingspeak_keys.RASPBERRY_PI2
thingspeak_data     = {}

# Tutorial for Matplotlib

# See http://www.labri.fr/perso/nrougier/teaching/matplotlib/ 

# arduino
PORT = '/dev/ttyUSB0'
BAUD =  115200
port = serial.Serial(PORT,BAUD) 

 
ydata = [0] * 50
ydata1 = [0] * 50

 
# make plot
#plt.ion() # set plot to animated
#fig = plt.figure()
#ax1 = fig.add_subplot(2, 2, 1)
#ax1.set_xlabel('#')
#ax1.set_title('Feinstaub')
#ax1.xaxis.set_major_locator(ticker.MaxNLocator(5))
#ax1.xaxis.set_minor_locator(ticker.MaxNLocator(10))
#ax1.yaxis.set_major_locator(ticker.MaxNLocator(5))
#ax1.yaxis.set_minor_locator(ticker.MaxNLocator(10))
#line, = plt.plot(ydata, color ='r')
#plt.legend([line], ['$\mu$g/m^3'])
#plt.grid(True)
#ax2 = fig.add_subplot(2, 2, 2)
#ax2.set_xlabel('#')
#ax2.set_title('Sensorspannung')
#ax2.xaxis.set_major_locator(ticker.MaxNLocator(5))
#ax2.xaxis.set_minor_locator(ticker.MaxNLocator(10))
#ax2.yaxis.set_major_locator(ticker.MaxNLocator(5))
#ax2.yaxis.set_minor_locator(ticker.MaxNLocator(10))
#line1, = plt.plot(ydata1, color = 'g')
#plt.legend([line1], ['Volt'])
#plt.grid(True)

def sumdata(dust,voltage):
    data=dust
    data1=voltage
    ydata.append(data)
    ydata1.append(data1)
    del ydata[0]
    del ydata1[0]
    return sum(ydata), sum(ydata1)

def plotdata():
    ymin = 0. #float(min(ydata))#-10
    ymax = float(max(ydata))+20
    ax1.set_ylim(ymin, ymax)
    ymax = float(max(ydata1))+2
    ax2.set_ylim(ymin, ymax)
    line.set_xdata(np.arange(len(ydata)))
    line.set_ydata(ydata)  # update the data
    line1.set_ydata(ydata1)  # update the data1
    plt.draw() # update the plot

def readSensors(port):
    # =====================
    # read from serial port 
    if port.inWaiting()>0:
           try: 
               rcv = port.readline().decode().replace('\n', '').replace('\r', '')
           except(ValueError):
               print("Redline Error")
           return rcv.split(',')
 
def lread():
# =============================
# ignore the first 100 readings
    i = 100
    while i>1:
          values = readSensors(port)      
          # print(values)
          i=i-1


lread()
# start data collection
counter = 0
while True:
       # read from serial port 
       values = readSensors(port)
       if values:           
           try:
               # =========================================
               # increase counter 
               counter = counter + 1
               # =========================================   
               # convert to float
               dust=1000.0 * ast.literal_eval(values[0]) # microgramm / m^3
               voltage=ast.literal_eval(values[1])
               # =========================================
               # plot data
               mdata = sumdata(dust,voltage)
               #plotdata()
               # print(ydata,counter)
               # ==========================================
                   # populate the thingspeak content dictionary 
               if counter > 50: 
                   ostemp = os.popen('vcgencmd measure_temp').readline()
                   temp = (ostemp.replace("temp=", "").replace("'C\n", ""))
                   dust=mdata[0]/50.
                   voltage = mdata[1]/50.
                   print((dust, voltage,temp))
                   thingspeak_data['field1'] = dust
                   thingspeak_data['field2'] = voltage
                   thingspeak_data['field3'] = temp
                   # ==========================================
                   # update thingspeak and reset counter
                   thingspeak.post(TS_KEY, thingspeak_data)
                   counter = 0                 
           # ==============================================
           # no data from sensor
           except:
               print('Sensor Read Error')
       # =================================================
       # wait 20 seconds
       # time.sleep(1)
    


