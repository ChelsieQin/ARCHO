/*
  Archo_SPLM.h - Library for Archo sound pressure level meter 1.0.
  Created by Lambda acoustics
*/
#ifndef Archo_SPLM_h
#define Archo_SPLM_h

#include "Arduino.h"
#include "Wire.h"

/* Address */
#define ADDR_TONE_FREQ 1

#define ADDR_IN_MUTE_SWITCH 22
#define ADDR_ON_OFF_SWITCH_TONE 23
#define ADDR_ON_OFF_SWITCH_WHITE 24
#define ADDR_ON_OFF_SWITCH_PINK 25

#define ADDR_IN_GAIN_IIR 27
#define ADDR_OUT_GAIN  26

#define ADDR_FIR_COEF 29

#define ADDR_FILTER_SELECT_Z_WEIGHT 177
#define ADDR_FILTER_SELECT_A_WEIGHT 178
#define ADDR_FILTER_SELECT_C_WEIGHT 179
#define ADDR_FILTER_SELECT_CUSTOM 180

/* Address end */

/*Command */
#define COMMAND32BIT 5

#define TONE_BASEFREQ 0x0000015E
#define ON 0x00800000
#define OFF 0x00000000
#define TONE	0 
#define WHITE_NOISE 1
#define PINK_NOISE 2 

#define DB_0   0x00800000 //1.0
#define DB_N3  0x005A9C78 //0.7079
#define DB_N6  0x00402752 //0.5012 
#define DB_N9  0x002D6A16 //0.3548
#define DB_N12 0x00202752 //0.2512
#define DB_N15 0x0016C227 //0.1778
#define DB_N18 0x00101D7E //0.1259
#define DB_N20 0x000CCCCD //0.1
#define DB_N21 0x000B67A1 //0.0891

#define SPL_PREFIX 11.7
#define LEVEL_FAST 8
#define LEVEL_SLOW 7 

#define Z_WEIGHT 0
#define A_WEIGHT 1
#define C_WEIGHT 2


class Archo 
{
    public:
    Archo(int addr);
    void begin();
    void write8bit(byte data);
    unsigned int  read8bit();
    void outVolume(unsigned long volume);
    void out32bit(byte addr,unsigned long data);
    void outMode(unsigned long signal_type);
    void outFreq(unsigned long freq);
    float getspl(float cal_data);
    void spl_switch(byte fast_or_slow);
    void spl_filter(byte filter_type);
    void spl_filter_custom(unsigned  long fir_coef[],int length);
    void spl_in_mute(unsigned long onoff);
    private:
    int _addr;
};
 
#endif

