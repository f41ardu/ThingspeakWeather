#!/usr/bin/env pyhton
# -*- coding: utf-8 -*-

#
# "THE WHISKEY-WARE LICENSE" (Revision ln(e))
# <tom@hash-n-bush.de> schrieb diese Datei. Solange Sie diesen Vermerk
# nicht entfernen, können Sie mit dieser Phyton Code machen was Sie wollen.
# Dieser Quelltext ist frei, so wie "frei" in "Die Gedanken sind frei". 
# Sollten wir uns eines Tages treffen und Sie denken, das ist es wert, dann
# geben Sie mir einen Whisky aus. tom.#-n-bush
#
#

# --- thr 2017-07-15 physical::computing AG SGH / Holzgerlingen 
# v 1.3
# Lesen und schreiben von mehren Datenfeldern
# 
# 
# readarduino.py
# 
# dependency: a library file containing the thingspeak api keys 
# 'thingspeak_keys.py' containing eg:
# RASPBERRY_PI2  = "KEYABCXYZETECETC"
# thr / 2017-07-11

# ======================================================================
import serial
import time
import ast

# import my local modules
import thingspeak_keys
import thingspeak

# thingspeak api key & data dictionary
TS_KEY              = thingspeak_keys.RASPBERRY_PI2
thingspeak_data     = {}

# arduino
PORT = '/dev/ttyUSB0'
BAUD =  9600
port = serial.Serial(PORT,BAUD)
dustSum = 0.0
counter= 1

def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        
        rv += ch.decode('ascii')
        if ch=='\r' or ch=='':
            return rv

def readSensors():
      
    port.write("\r\n")
    try: 
       rcv = readlineCR(port)
        
       rcv.replace('\r','').replace('\n','').replace('\'','').replace('\'','').replace('\'','')
       values = rcv.split(',')
       # convet char to float
       dust=ast.literal_eval(values[0])
       voltage=ast.literal_eval(values[1])

       print((dust, voltage))
       # ======================================================================
       # populate the thingspeak content dictionary
       thingspeak_data['field1'] = dust
       thingspeak_data['field2'] = voltage
       #    thingspeak_data['field3'] = data3
       #    thingspeak_data['field4'] = data4
       #    thingspeak_data['field5'] = data5
       #    thingspeak_data['field6'] = data6
       #    thingspeak_data['field7'] = data7
       #    thingspeak_data['field8'] = data8
       # ======================================================================

       # POST to thingspeak
       
       thingspeak.post(TS_KEY, thingspeak_data)
            
    except:
        print ("Serial connection failed")
    
# main program 
if __name__ == "__main__":
    readlineCR(port)
    while True:
        print(":: Thinkspeak POST:")
        readSensors()
        time.sleep(20)
    
