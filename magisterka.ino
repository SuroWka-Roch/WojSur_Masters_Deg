#ifndef _SAM3XA_
#define _SAM3XA_

#if defined (__SAM3A4C__)
#include "sam3a4c.h"
#elif defined (__SAM3A8C__)
#include "sam3a8c.h"
#elif defined (__SAM3X4C__)
#include "sam3x4c.h"
#elif defined (__SAM3X4E__)
#include "sam3x4e.h"
#elif defined (__SAM3X8C__)
#include "sam3x8c.h"
#elif defined (__SAM3X8E__)
#include "sam3x8e.h"
#elif defined (__SAM3X8H__)
#include "sam3x8h.h"
#endif

#endif /* _SAM3XA_ */

#define SYSCLC *(volatile uint32_t *) 0x400E0610 // i canot find the clc makro 
#define clc_pin_num 19
#define clc_pin_val 0x1<<clc_pin_num  //2^19

//int clc_pin_num = 19;
//int clc_pin_val = 0x1<<clc_pin_num;

//clc to 44 pin c.19 
//data pins start at pin 33 

int tab[8] = {0};
int val;

volatile unsigned int counts[8] = { 0 };
int pin_mask = 0B1111<<1;
int i=0,f=0;
void setup() {
  Serial.begin(9600);
  REG_PIOC_ODR = pin_mask;//disable output of pins
  REG_PIOC_OER = clc_pin_val; // enable output
  REG_PIOC_PUDR = 0B1<<clc_pin_num|pin_mask;// pull up disable 
  SYSCLC = 1<<13; //REG_PMC_PCER0 = 1<<13;
}
void loop() {
  //read value on bus
  for(f=0;f<1E5;f++){
    for(i=0;i<8;i++){
      //send sygnal to clc
      REG_PIOC_SODR = clc_pin_val;
      //read value and add it to table 
      //counts[i] += (REG_PIOC_PDSR&pin_mask)>>1;
      val = (REG_PIOC_PDSR&pin_mask)>>1;
      if(tab[i]< val){
          counts[i] += val-tab[i];
      }
      else{
          counts[i] += val+16-tab[i];
      }
      tab[i]= val;
      //turn of clc 
      REG_PIOC_CODR = clc_pin_val;
    }
    REG_PIOC_SODR = clc_pin_val;
    REG_PIOC_CODR = clc_pin_val;
  }
  
  for(i=0;i<8;i++){
    Serial.println(counts[i]);
    counts[i]=0;
  }
  
  
 
}
