#!/usr/bin/pyhton

#
# --- thr 2017-07-11 physical::computing AG SGH / Holzgerlingen 
# v 1.0

# updateThinkspeak.py
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
        rv += ch
        if ch=='\r' or ch=='':
            return rv

rcv = readlineCR(port)

while True:
#    port.write("\r\nSay something:")
    rcv = readlineCR(port)
    rcv.replace('\r','').replace('\n','').replace('\'','').replace('\'','').replace('\'','')
    dust=ast.literal_eval(rcv)
#    dustSum=dustSum
    print((dust))
    # ======================================================================
# populate the thingspeak content dictionary
    thingspeak_data['field1'] = dust
#    thingspeak_data['field2'] = data2
#    thingspeak_data['field3'] = data3
#    thingspeak_data['field4'] = data4
#    thingspeak_data['field5'] = data5
#    thingspeak_data['field6'] = data6
#    thingspeak_data['field7'] = data7
#    thingspeak_data['field8'] = data8
# ======================================================================
# POST to thingspeak
    print(":: Thinkspeak POST:")
    thingspeak.post(TS_KEY, thingspeak_data)
    time.sleep(20)
