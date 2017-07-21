import serial
import ast
import numpy as np
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt

# Tutorial
# See http://www.labri.fr/perso/nrougier/teaching/matplotlib/ 

# arduino
PORT = '/dev/ttyUSB0'
BAUD =  115200
port = serial.Serial(PORT,BAUD) 
plt.ion() # set plot to animated
 
ydata = [0] * 100
ydata1 = [0] * 100
ax1=plt.axes()
 
# make plot
plt.subplot(2, 2, 1)
line, = plt.plot(ydata)
plt.subplot(2, 2, 2)
line1,= plt.plot(ydata1)
plt.ylim([0,10])


plt.legend([line, line1], ['mg/m^3', 'Volt'])



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
i = 10
while i>1:
      values = readSensors(port)      
      #print(values)
      i=i-1

# start data collection
while True: 
       # read from serial port 
       values = readSensors(port)
       if values:
           try:
               # ==========================================   
               # convert to float
               dust=ast.literal_eval(values[0])
               voltage=ast.literal_eval(values[1])
               #dust=values[0]
               #voltage=values[1]
               # ==========================================
               #print((dust, voltage))
               
               data=dust
               data1=voltage
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


    


