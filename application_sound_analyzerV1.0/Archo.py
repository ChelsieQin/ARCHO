## Archo Sound analyzer V1.0
##     Lambda Acoustics
##        2015.12

import sys
import os
import time
import usb
import threading
import struct


class Archo:
    def __init__(self,Frames):
       self._Init = False
       self._Running = False
       self._Frames = Frames
       self._DataAvaliable = False 
       
       self._busses = usb.busses()
       self._rdev = None
       self._observers = []
       for bus in self._busses:
           for dev in bus.devices:
               if dev.idVendor == 0x2c51 :
                  self._rdev = dev
           if self._rdev==None:
              print "Archo not find !"
              sys.exit()
           else:
              self._dev = self._rdev
              self._Init = True
              self._current_handle = self._dev.open()
              self._dev.dev.read(0x86,512*3,0,2000)
          
    def add_observer(self,observer):
        self._observers.append(observer)
        
    def _get_audio_frame(self): 

        while self._Running:
            data = self._dev.dev.read(0x86,512*self._Frames,0,2000)
            self._rdata = struct.unpack(str(len(data)/2)+'h',data)
            self._length_rdata = len(self._rdata)

            for observer in self._observers:
                observer.update(self._rdata)
            
    def start(self):
        
        print "Archo start!"
        try:
            archo_thread = threading.Thread(target=self._get_audio_frame)
            self._Running = True
            archo_thread.start()
            

        except Exception, e:
            print "Archo failure:", str(e)

    def stop(self):

        print "Archo stop!"
        self._Running = False
        time.sleep(1)
        self._dev.dev.reset()
        
       

