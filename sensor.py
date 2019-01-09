#!/usr/bin/python
# -*- coding: UTF-8 -*-

import serial, time, struct

def toString(string):
    try:
        return string.decode("utf-8")
    except ValueError:
        return string

ser = serial.Serial()
ser.port = "COM10" # Set this to your serial port
ser.baudrate = 9600

ser.open()
ser.flushInput()

byte, lastbyte = b"\x00", "\x00"

while True:
    lastbyte = byte
    byte = ser.read(size=1)
    #print("lastbyte: ",lastbyte, " | byte: ",byte, "\n")
    # We got a valid packet header
    if lastbyte == b"\xaa" and byte == b"\xc0":
        sentence = ser.read(size=8) # Read 8 more bytes
        readings = struct.unpack('<hhxxcc',sentence) # Decode the packet - big endian, 2 shorts for pm2.5 and pm10, 2 reserved bytes, checksum, message tail

        pm_25 = readings[0]/10.0
        pm_10 = readings[1]/10.0
        # ignoring the checksum and message tail

        print ("PM 25: ", pm_25, " [ug/m^3]")
        print ("PM 10: ", pm_10, "[ug/m^3]\n")
        