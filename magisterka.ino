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

#define SYSCLC *(volatile uint32_t *) 0x400E0610 // I can't find the clc makro - Register for perifrel clc control
#define NOP __asm__("nop")


/**************************************************************************************/

//communication constants
#define HANSHAKE_CONFIRM_REQUEST_CODE '420'
#define HANSHAKE_CONFIRMATION_CODE '421'
#define CHOOSE_MULTIPLEXER_CODE 'cmx'
#define AKW_TIME_MS_CODE 'atm'
#define START_CODE 'srt'
#define STOP_CODE 'stp'

//CONFIG


#define STARTING_MULTIPLEXER_STATE 0

//4.618us per circle 
#define CIRCLES_FOR_1MS (21656.0/100.0)
#define DEAD_TIME_CORRECTION (1.14503073835)


//All output is done on periferal PC 

#define CLC_PIN_NUM 19 //Arduino pin 44
#define CLC_PIN_VAL 0x1<<CLC_PIN_NUM  //2^19

#define MULTIPLEXER_PIN_NUM 18 //Arduino pin 45
#define MULTIPLEXER_PIN_VAL 0x1<<MULTIPLEXER_PIN_NUM  

#define CLEAR_PIN_NUM 17 //Arduino pin 46
#define CLEAR_PIN_VAL 0x1<<CLEAR_PIN_NUM 

//Global values 
double akw_time = 1.0;
int multiplexer_state_flag = STARTING_MULTIPLEXER_STATE;
volatile unsigned int* counts = NULL;
volatile unsigned int* multiplexerPointers[2]; 
int pin_mask = 0B1111<<1; //PC0 is NC, data pins start at arduino pin 33 


void(* resetFunc) (void) = 0;//declare reset function at address 0

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
  REG_PIOC_OER = CLC_PIN_VAL | MULTIPLEXER_PIN_VAL | CLEAR_PIN_VAL; // enable output
  REG_PIOC_PUDR = 0B1<<CLC_PIN_NUM | MULTIPLEXER_PIN_VAL | pin_mask | CLEAR_PIN_VAL;// pull up disable 
  SYSCLC = 1<<13; //PMC Peripheral Clock Enable Register 0, turn on a periferal clock 

  set_multiplexer(STARTING_MULTIPLEXER_STATE);
}


void loop() {


  aquisition(akw_time);
  write_output();

}


void aquisition(double time){
  /**
   * @brief Will count and reset counters on external hardwere. Fills counters table.
   * @param time aquisition time is equal to time in ms
   * 
  */
  int i=0,f=0,val;
  int booleenCounter;
  int previousValue[8]={0};

  REG_PIOC_CODR = CLEAR_PIN_VAL;
  REG_PIOC_SODR = CLEAR_PIN_VAL; //Reset value on counter - idk if realy needed - probably due to removal
  
  noInterrupts(); 


  //read value on bus
  for(f=0;f< (int)(CIRCLES_FOR_1MS * DEAD_TIME_CORRECTION * time); f++){
    for(i=0;i<8;i++){
      
      REG_PIOC_SODR = CLC_PIN_VAL; //send signal to clc, change is triggered on rinsing edge but time is needed for hardwere to set it's state
      REG_PIOC_CODR = CLC_PIN_VAL; //turn of clc
      
      val = (REG_PIOC_PDSR & pin_mask)>>1; //read value and add it to table 

      /*
      * Dealing with counters overflow:
      *   table previousValue has value of last state
      *   If previous state is bigger calculate overflow 
      */

      if(previousValue[i] <= val){ 
          counts[i] += val - previousValue[i];
      }
      else{
          counts[i] += val + 16 - previousValue[i]; //15 is max for 4 bit counters but 16 gives value of 1 for 0 state  
      }

      previousValue[i]= val; 

    }

  
    REG_PIOC_SODR = CLC_PIN_VAL; //reset clc empty shift register circle 
    REG_PIOC_CODR = CLC_PIN_VAL;
  
  }


  interrupts();
}

void write_output(){
  /**
   *  @brief print output to serial port 
   */

  for(int i=0;i<8;i++){
    Serial.println(counts[i]);
    counts[i]=0;
  }
  
  Serial.println("~~~~~~~~~~~~~");
  Serial.flush();

}

void set_multiplexer(int state_to_set){

  if(state_to_set){
    REG_PIOC_SODR = MULTIPLEXER_PIN_VAL; // set begining multiplexer state for LOW.
  }
  else{
    REG_PIOC_CODR = MULTIPLEXER_PIN_VAL; // set begining multiplexer state for LOW.
  }
  multiplexer_state_flag = state_to_set;

}