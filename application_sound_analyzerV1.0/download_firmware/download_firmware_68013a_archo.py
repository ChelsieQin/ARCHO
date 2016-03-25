from numpy import *
import sys
import os
import time
import usb
from lib_local.hexreader import *

##################################
bootfile = 'Vend_Ax.hex'
firmware = 'Firmware.iic'
##################################

# find all of the USB busses
busses = usb.busses()

rdev = None
for bus in busses:
    for dev in bus.devices:
        if dev.idVendor == 0x04B4 :
       		 rdev = dev
if rdev==None:
	print "Could not find a CY7C68013\ndev.idVendor == 0x04B4 and dev.idProduct == 0x8613"
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
time.sleep(0.1)
##def ctrl_transfer(self, bmRequestType, bRequest, wValue=0, wIndex=0,
##            data_or_wLength = None, timeout = None):
filename = bootfile
hexfile = open(filename,'r')


for line in hexfile.readlines():
    if len(line) > 12 :
        addr,data,lenth = process_hex_line(line)
        #print 'addr:',addr,' length:',lenth
        current_handle.controlMsg(requestType, request,data,addr, index, timeout)
time.sleep(0.1)

current_handle.controlMsg(requestType, request, unreset, value, index, timeout)        

hexfile.close()
print 'boot done,begin download Firmware of 68013a\n'
time.sleep(2)
print 'begin download\n'

filename = firmware
iicfile = open(filename,'rb')
iic_rawdata = ''
for i in iicfile:
    iic_rawdata += i
    
requestType = 0x40
request = 0xa9
data = iic_rawdata
wValve = 0
windex = 1<<4

current_handle.controlMsg(requestType, request, data, wValve, windex, 1000)

time.sleep(2)

print '68013A firmware download successfully!'

