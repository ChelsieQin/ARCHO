/*
  Archo_SPLM.cpp - Library for Archo sound pressure level meter 1.0.
  Created by Lambda acoustics

*/
 
#include "Arduino.h"
#include "Archo_SPLM.h"
//#include "Wire.h"
 
Archo::Archo(int addr)
{
 _addr = addr ;
}

void Archo::begin()
{
 Wire.begin();
}

void Archo::write8bit(byte data)
{
     Wire.beginTransmission(_addr); // transmit to device #4
     Wire.write(data);              // sends one byte  
     Wire.endTransmission();    // stop transmitting
     delay(5);
     Wire.requestFrom(_addr, 1);    // request 6 bytes from slave device #2

     while(Wire.available())    // slave may send less than requested
     { 
      char c = Wire.read(); // receive a byte as character
     }
     delay(5);  
   
}
 
unsigned int  Archo::read8bit()
{    unsigned int c ;
     Wire.requestFrom(_addr, 1);    // request 6 bytes from slave device #2
     while(Wire.available())    // slave may send less than requested
     { 
       c = Wire.read(); // receive a byte as character
     }
    delay(1);
    Wire.requestFrom(_addr, 1);    // request 6 bytes from slave device #2
    while(Wire.available())    // slave may send less than requested
    { 
      char c1 = Wire.read(); // receive a byte as character
     }
    delay(1);
    return c ;
   
}

float Archo::getspl(float cal_data){

      unsigned int data1,data2 ;
      float data ;
      write8bit(1);
      read8bit();
      write8bit(2);
      read8bit();
      write8bit(3);
      data1 = read8bit();
      write8bit(4);
      data2 = read8bit();
   
   
      data = data2*25.6+data1/10.0 +cal_data + SPL_PREFIX;
     
      return data ;
}

void  Archo::spl_switch(byte fast_or_slow)
{ 
      write8bit(fast_or_slow);
}

void  Archo::outVolume(unsigned long volume)
{ 
      out32bit(ADDR_OUT_GAIN,volume);
}

void  Archo::out32bit(byte addr,unsigned long data)
{ 
	write8bit(COMMAND32BIT);
	write8bit(0x00);
	write8bit(addr);
        write8bit(data >> 24);
	write8bit((data & 0x00FF0000) >> 16);
	write8bit((data & 0x0000FF00) >> 8);
	write8bit((data & 0x000000FF));
	delay(10);
}

void  Archo::spl_in_mute(unsigned long onoff){
        out32bit(ADDR_IN_MUTE_SWITCH,onoff);
      }

void  Archo::spl_filter(byte filter_type){
      switch (filter_type){
		 case A_WEIGHT: 
		      out32bit(ADDR_FILTER_SELECT_A_WEIGHT,ON);
		      out32bit(ADDR_FILTER_SELECT_C_WEIGHT,OFF);
		      out32bit(ADDR_FILTER_SELECT_Z_WEIGHT,OFF);
		      break;
		 case C_WEIGHT:
		      out32bit(ADDR_FILTER_SELECT_A_WEIGHT,OFF);
		      out32bit(ADDR_FILTER_SELECT_C_WEIGHT,ON);
		      out32bit(ADDR_FILTER_SELECT_Z_WEIGHT,OFF);
		      break;
		 case Z_WEIGHT:
		      out32bit(ADDR_FILTER_SELECT_A_WEIGHT,OFF);
		      out32bit(ADDR_FILTER_SELECT_C_WEIGHT,OFF);
		      out32bit(ADDR_FILTER_SELECT_Z_WEIGHT,ON);
		      break;
		 default:
		
                 break;
		}
     
}

void  Archo::spl_filter_custom(unsigned long fir_coef[],int length){
      
      int i = 0 ;
      spl_in_mute(OFF) ;
      for(i = 0;i < length ;i++){
	     out32bit(ADDR_FIR_COEF+i,fir_coef[i]);
	    
      }
      
       out32bit(ADDR_FILTER_SELECT_A_WEIGHT,OFF);
       out32bit(ADDR_FILTER_SELECT_C_WEIGHT,OFF);
       out32bit(ADDR_FILTER_SELECT_Z_WEIGHT,OFF);
      out32bit(ADDR_FILTER_SELECT_CUSTOM,ON);
      spl_in_mute(ON) ;
	
}

void Archo::outFreq(unsigned long freq)
{
	out32bit(ADDR_TONE_FREQ,freq*TONE_BASEFREQ);
}
void Archo::outMode(unsigned long signal_type)
{
	switch (signal_type)
		{
		 case TONE: 
			 out32bit(ADDR_ON_OFF_SWITCH_TONE,ON) ;
			 out32bit(ADDR_ON_OFF_SWITCH_WHITE,OFF) ;
			 out32bit(ADDR_ON_OFF_SWITCH_PINK,OFF) ;
			 break;
		 case WHITE_NOISE:
		         out32bit(ADDR_ON_OFF_SWITCH_TONE,OFF) ;
			 out32bit(ADDR_ON_OFF_SWITCH_WHITE,ON) ;
			 out32bit(ADDR_ON_OFF_SWITCH_PINK,OFF) ;
			 break;
		 case PINK_NOISE: 
			 out32bit(ADDR_ON_OFF_SWITCH_TONE,OFF) ;
			 out32bit(ADDR_ON_OFF_SWITCH_WHITE,OFF) ;
			 out32bit(ADDR_ON_OFF_SWITCH_PINK,ON) ;
			 break;
		 default: 
                 break;
		}
   
}


