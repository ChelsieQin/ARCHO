# -*- coding: utf-8 -*-
from numpy import *
import sys
import os
import time
import usb
from lib_local.hexreader import *

##################################
bootfile = 'boot.hex'
firmware = 'output_file.txt'
##################################

# find all of the USB busses
busses = usb.busses()

rdev = None
for bus in busses:
    for dev in bus.devices:
        if dev.idVendor == 0x04B4 :
       		 rdev = dev
if rdev==None:
	print "Could not find a Archo"
	sys.exit()
else:
        print "find device,booting ..."
	dev = rdev

current_handle = dev.open()

requestType = 0x40
request = 0xa0
value=0xe600
index=0
timeout=1000
reset = [0x01]
unreset = [0x00]

current_handle.controlMsg(requestType, request, reset, value, index, timeout)
time.sleep(0.5)

filename = bootfile
hexfile = open(filename,'r')


for line in hexfile.readlines():
    if len(line) > 12 :
        addr,data,lenth = process_hex_line(line)
        #print 'addr:',addr,' length:',lenth
        current_handle.controlMsg(requestType, request,data,addr, index, timeout)
time.sleep(0.5)

current_handle.controlMsg(requestType, request, unreset, value, index, timeout)        

hexfile.close()
print 'boot done,begin download Firmware of DSP&FPGA\n'
time.sleep(3)
print 'begin download\n'

# find all of the USB busses
busses = usb.busses()
rdev = None
for bus in busses:
    for dev in bus.devices:
        if dev.idVendor == 0x2c51 :
       		 rdev = dev
if rdev==None:
	print "Could not find a Archo-boot"
	sys.exit()
else:
	dev = rdev

endpoint=8
current_handle = dev.open()
rdev.dev.write(0x2,'\x12',0,8000)
time.sleep(1)
b = '\x00'*512
b = rdev.dev.read(0x86,51200,0,4000)

while(b[0] != 0):
     b = rdev.dev.read(0x86,51200,0,4000)
     b[0:128:1]
     print 'clear spiflash , waiting ... '



fi = open(firmware,'rb')
b = fi.readlines()
s = len(b)
bufbanks = linspace(0,s-1,s)
a = ''
for i in bufbanks:
    indez  = int(i)
    a = a + b[indez]
    
a = a[0:len(a)]
buflen = len(a)
buflen = 512
bufs = len(a)/buflen
bufbanks = linspace(0,bufs,bufs+1)

for i in bufbanks:
      
    bufindex = i*buflen
    
    bufindex = int(bufindex)
    b = a[bufindex:(bufindex+buflen)]
     
    rdev.dev.write(0x4,b,0,8000)
    #print 'bank',i,' from', bufindex,' to',bufindex+buflen
    print 'block:',i,' of',bufs,',',int((i)*100/bufs),"% finished"
    time.sleep(0.01)
      

time.sleep(2)
rdev.dev.write(0x2,'\x10')

rdev.dev.reset
print 'DSP&FPGA firmware download successfully!'

