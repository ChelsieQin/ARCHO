##          Demo: real-time analyzer
##     ( Base on FFT and Hanning window)
##            Lambda Acoustics
##               2015.12
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.signal as signal

import Archo as Archo


class RTA:
    def __init__(self,calibration,size):
        self._calibration = calibration
        self._fftsize = size
        self._fftvalue = range(size/2);
        
    def update(self,data):
        length = len(data)
        #data = data*np.hamming(self._fftsize)
        data = data*np.hanning(self._fftsize)
        fft_data = (np.fft.fft(data)/(len(data)/2))
        b = fft_data[0:(len(data)/2)]
        self._fftvalue = 20*np.log10((abs(b)))+self._calibration
        
    def read_fftvalue(self):
        return self._fftvalue

if __name__ == '__main__':

   N = 4096
   fig, ax = plt.subplots()
   plt.xlabel('freq (Hz)')
   ax.set_ylabel('SPL (dB)')
   freq = np.linspace(0,24000,N/2)
   line, = ax.semilogx(freq,range(N/2))
   ax.set_ylim(0,120)
   ax.grid()
   
   
   archo = Archo.Archo(N/256)
   rta = RTA(34.4,N)
   archo.add_observer(rta)
   archo.start()

   def animate(i):
        global rta
        line.set_ydata(rta.read_fftvalue())
        
        
   ani = animation.FuncAnimation(fig, animate, 50, repeat=True)
   plt.show()
   archo.stop()
