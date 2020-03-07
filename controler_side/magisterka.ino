#include <stdlib.h>
#include <string.h>
#include "ENV_CONFIG.h"
#include "USER_CONFIG.h"

//Global values 
double akw_time = 1000.0; // In ms
int multiplexer_state_flag = STARTING_MULTIPLEXER_STATE;
volatile unsigned int* counts = NULL;
volatile unsigned int* multiplexerPointers[2]; 
int pin_mask = 0B1111<<1; //PC0 is NC, data pins start at arduino pin 33 
char received_buffer[RECEIVED_BUFFER_SIZE];
char* command_pointer = received_buffer;
int hibernation_flag = 0;
int command_in_buffer_flag = 0;




void setup() {
  Serial.begin(SERIAL_SPEED);

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

  if(!hibernation_flag){ 
    aquisition(akw_time);
    write_output();
  }
  receive_command();

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
      *   Dealing with counters overflow:
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
    REG_PIOC_SODR = MULTIPLEXER_PIN_VAL; // set begining multiplexer state for HIGH.
  }
  else{
    REG_PIOC_CODR = MULTIPLEXER_PIN_VAL; // set begining multiplexer state for LOW.
  }

  multiplexer_state_flag = state_to_set;

}

void receive_command(){
  if(!command_in_buffer_flag){
    command_pointer = received_buffer;
  }

  while(Serial.available() > 0)
  {
    Serial.println(Serial.available());
    command_in_buffer_flag = 1;
    *command_pointer = Serial.read();
    if(*command_pointer == COMAND_ENDING_CONST){
      Serial.print(received_buffer);
      analyze_command();
    }
    command_pointer++;
  }

  if(Serial.available()){
    receive_command();
  }

}

void analyze_command(){

  if(!strcmp(received_buffer, HANSHAKE_CONFIRM_REQUEST_CODE)){
    Serial.println( HANSHAKE_CONFIRMATION_CODE );
  }else{
    
  if(!strcmp( received_buffer, CHOOSE_MULTIPLEXER_CODE )){
    int set_flag = read_number();
    set_multiplexer(set_flag);
  }else{

  if(!strcmp( received_buffer, AKW_TIME_MS_CODE)){
    akw_time = read_number();
  }else{
    ;
  }
  }
  }

  // Serial.println(received_buffer);
  command_in_buffer_flag = 0;
  
}

int read_number(){
  char* command_pointer = received_buffer;
  while(!Serial.available());
  while (Serial.available() > 0){
    *command_pointer = Serial.read();
    if(*command_pointer == COMAND_ENDING_CONST){
      break;
    }
    command_pointer++;
  }
  return atoi(received_buffer);
}
