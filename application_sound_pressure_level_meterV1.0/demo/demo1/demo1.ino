#include <Archo_SPLM.h>
#include <Wire.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(8, 13, 9, 4, 5, 6, 7);
Archo archo(77) ;

void setup()
{
  archo.begin();
  //wait 4 sec, archo init
  delay(4000);
  // 1000Hz/-3dBFS sin wave at archo's output2 ( right channel )
  archo.outMode(TONE); 
  archo.outFreq(1000); 
  archo.outVolume(DB_N3);
  
  archo.spl_filter(A_WEIGHT);
  archo.spl_switch(LEVEL_SLOW);
  
 }
void loop(){
  lcd.setCursor(0,0); 
  //mic caliration value is 36.3,
  //if use +20dB jumper, use 16.3 ( 36.3 - 20 = 16.3)  
  lcd.print(archo.getspl(36.3)); 
  delay(500); 
}
