#include <stdlib.h>

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

#define SYSCLC *(volatile uint32_t *) 0x400E0610    // I can't find the clc makro - Register for perifrel clc control
#define LOAD *(volatile uint32_t *) 0xE000E014      // Register defining value that system procesor loads when restarted - gives timer of milisecunds WO max 16777215
#define CTRL *(volatile uint32_t *) 0xE000E018      // At 16 there is a flag wheter clc reached 0 here are adidional options. RW
#define RELOAD *(volatile uint32_t *) 0xE000E018    // Writing anything in this register sets it to 0 sets TIMER_FLAG to 0 so it loads LOAD value.
#define PIOC_OWDR *(volatile uint32_t *) 0x400E12A4 // Protect lines from writes on PIOC_ODSR, kind of a mask.
#define PIOC_ODSR *(volatile uint32_t *) 0x400E1238 // Cool write register writen value is put on IO line
 
/**************************************************************************************/

//All output is done on periferal PC 

#define CLC_PIN_NUM 19 //Arduino pin 44
#define CLC_PIN_VAL 0x1<<CLC_PIN_NUM  //2^19

#define MULTIPLEXER_PIN_NUM 18 //Arduino pin 45
#define MULTIPLEXER_PIN_VAL 0x1<<MULTIPLEXER_PIN_NUM  

#define CLEAR_PIN_NUM 17 //Arduino pin 46
#define CLEAR_PIN_VAL 0x1<<MULTIPLEXER_PIN_NUM 

#define ACQUISITION_TIME_MS 10000 /must be int 
#define TIMER_FLAG CTRL & (0B1<<16)


volatile unsigned int* multiplexerPointers[2]; 

//volatile unsigned int counts[16] = { 0 };
volatile unsigned int* counts = NULL;
int pin_mask = 0B1111<<1; //PC0 is NC, data pins start at arduino pin 33 

void setup() {
  Serial.begin(9600);

  /* Using pointers to table as a way to deal witch multiplexing with low procesor yeald */
  counts = (unsigned int *) calloc(16, sizeof( unsigned int ));  

  if (counts == NULL){
    resetFunc(); //panic escape
  }

  multiplexerPointers[0]=counts;
  multiplexerPointers[1]=counts+8; //middle of table
  

  REG_PIOC_ODR = pin_mask;//disable output of pins
  REG_PIOC_OER = CLC_PIN_VAL | MULTIPLEXER_PIN_VAL | CLEAR_PIN_NUM; // enable output
  REG_PIOC_PUDR = 0B1<<CLC_PIN_NUM | MULTIPLEXER_PIN_VAL | pin_mask | CLEAR_PIN_VAL;// pull up disable 
  SYSCLC = 1<<13; //PMC Peripheral Clock Enable Register 0, turn on a periferal clock 
  REG_PIOC_CODR = MULTIPLEXER_PIN_VAL; // set begining multiplexer state for LOW. 
  cli(); // Test wheter this helps at all
  LOAD = ACQUISITION_TIME_MS;
  PIOC_OWDR = ~CLC_PIN_VAL; // makes PIOC_ODSR change value only for clc pin.  
}


void loop() {
  int i=0,f=0,val;
  int booleenCounter;
  int previousValue[8]={0};
  for(booleenCounter=0;booleenCounter<2;booleenCounter++){ //Multiplexer loop
    counts = multiplexerPointers[booleenCounter%2];
    booleenCounter%2 ? REG_PIOC_SODR = MULTIPLEXER_PIN_VAL:REG_PIOC_CODR = MULTIPLEXER_PIN_VAL; // choose muliplaxer - writes LOW to anything else

    //CODE
      //REG_PIOC_SODR = CLEAR_PIN_NUM; //Reset value on counter - idk if realy needed - probably due to removal
      //REG_PIOC_CODR = CLEAR_PIN_NUM;

    //read value on bus
    RELOAD = 1; //start the clock TIMER_FLAG
    while(!TIMER_FLAG){
      for(i=0;i<8;i++){
        
        PIOC_ODSR = CLC_PIN_VAL; //send sygnal to clc, change is trigered on rising edge but time is needed for hardwere to set it's state
        PIOC_ODSR = 0; //turn of clc - works because of PIOC_OWDR mask
        
        val = (REG_PIOC_PDSR & pin_mask)>>1; //read value and add it to table 

        /*
        * Dealing with counters overflow:
        *   table previousValue has value of last state
        *   If previous state is biger calcuate overflow 
        */

        if(previousValue[i] < val){ 
            counts[i] += val - previousValue[i];
        }
        else{
            counts[i] += val + 16 - previousValue[i]; //15 is max for 4 bit counters but 16 gives value of 1 for 0 state  
        }
        previousValue[i] = val; 

      }

      //CODE
        //PIOC_ODSR = CLC_PIN_VAL; //reset clc- might be not needed 
        //PIOC_ODSR = 0;

    }

  }

  /*print output to serial port */
  for(i=0;i<8;i++){
    Serial.println(counts[i]);
    counts[i]=0;
  }

}
