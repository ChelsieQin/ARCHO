## Demo: Sound pressure level meter 
##     Lambda Acoustics
##        2015.12

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Archo as Archo


class SPL_Meter:
    def __init__(self,calibration):
        self._calibration = calibration
        self._spl = 0 ;
        
    def update(self,data):
        length = len(data)
        self._spl = 10*np.log10(sum([ i*i for i in data])*1.0/length)+self._calibration

    def read_spl(self):
        return self._spl

if __name__ == '__main__':

   width = 0.8       # the width of the bars
   fig, ax = plt.subplots(figsize=(1,5))
   fig.subplots_adjust(left=0.5)
   splbar, = ax.bar(0.1, 0, width, color='b')

   ax.set_ylabel('SPL (dB)')
   ax.set_ylim(30,120)
   ax.set_xlim(-1,1)
   ax.grid()
   ax.xaxis.set_visible(False)
   
   archo = Archo.Archo(10)
   ## if use 'Mic in (+20dB)' setup,
   ## calibration value should be 33.7-20 = 13.7dB
   spl_meter = SPL_Meter(33.7)

   archo.add_observer(spl_meter)
   archo.start()

   def animate(i):
        global spl_meter
        spl = spl_meter.read_spl()
        #print  spl
        splbar.set_height(spl)
        
        
   ani = animation.FuncAnimation(fig, animate, 100, repeat=True)
   plt.show()
   archo.stop()
