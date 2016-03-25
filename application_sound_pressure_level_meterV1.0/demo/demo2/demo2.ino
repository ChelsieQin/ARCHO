#include <Archo_SPLM.h>
#include <Wire.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(8, 13, 9, 4, 5, 6, 7);

unsigned long fir_coef[] = {
0xccccc, //0.1
0xccccc, //0.1
0xccccc, //0.1
0x200000,//0.25
0x200000,//0.25
0x200000,//0.25
0x200000,//0.25
0x200000,//0.25
0x200000,//0.25
0x200000};//0.25

Archo archo(77) ;
void setup()
{
  archo.begin();
  //wait 4 sec, archo init
  delay(4000);
  // WHITE/-3dBFS pink_noise at archo's output2 ( right channel )
  archo.outMode(PINK_NOISE); 
  archo.outVolume(DB_N3);
  
  archo.spl_switch(LEVEL_FAST);
  archo.spl_filter(A_WEIGHT);
  archo.spl_filter_custom(fir_coef,10);
 }
void loop(){
  lcd.setCursor(0,0); 
  //mic caliration value is 36.3,
  //if use +20dB jumper, use 16.3 .( 36.3 - 20 = 6.3)
  lcd.print(archo.getspl(36.3)); 
  delay(100); 
}


