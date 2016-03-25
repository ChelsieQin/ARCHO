## Demo: Wave recorder using Archo
##     Lambda Acoustics
##        2015.12

import sys
import os
import time
import usb
import threading
import struct
import wave
import Archo

class Recorder:
    def __init__(self):
        filename =  "CH1_48kHz-"+time.ctime().replace(" ","-").replace(":","-")+".wav"
        self.wavfile = wave.open(filename, "wb")
        self.wavfile.setnchannels(1)
        self.wavfile.setsampwidth(2)
        self.wavfile.setframerate(48000)
        
    def update(self,data):
        c = ''
        for d in data:
           c = c + struct.pack('h',d)
        self.wavfile.writeframes(c)

    def close(self):
        self.wavfile.close()

if __name__ == '__main__':
    
   archo = Archo.Archo(10)
   recorder = Recorder()
   archo.add_observer(recorder)
   archo.start()

   time.sleep(10)
   archo.stop()
   recorder.close()
