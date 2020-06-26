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
int hibernation_flag = 1;
int command_in_buffer_flag = 0;




void setup() {
  SerialUSB.begin(SERIAL_SPEED);

  /* Using pointers to table as a way to deal witch multiplexing with low procesor yeald */
  counts = (unsigned int *) calloc(16, sizeof( unsigned int ));  

  if (counts == NULL){
    resetFunc(); //panic escape
  }

  multiplexerPointers[0]=counts;
  multiplexerPointers[1]=counts+8; //middle of table
  

  REG_PIOC_ODR = pin_mask;//disable output of pins
  //REG_PIOC_OER = CLC_PIN_VAL | MULTIPLEXER_PIN_VAL | CLEAR_PIN_VAL; // enable output
  REG_PIOD_OER = CLC_PIN_VAL | MULTIPLEXER_PIN_VAL | CLEAR_PIN_VAL;
  REG_PIOC_PUDR = (0B1<<CLC_PIN_NUM);// pull up disable 
  REG_PIOD_PUER = MULTIPLEXER_PIN_VAL | pin_mask | CLEAR_PIN_VAL;
  SYSCLC = 0B11<<13; //PMC Peripheral Clock Enable Register 0, turn on a periferal clock 

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
  volatile unsigned int* counts_pointer = counts;
  
  noInterrupts(); 

  for(int j = 0; j<2; j++){ // j is either 1 or 0 
    set_multiplexer(!j);
    counts_pointer = &counts[8*j];
    clear_int_table(previousValue,8);

    REG_PIOD_CODR = CLEAR_PIN_VAL;
    REG_PIOD_SODR = CLEAR_PIN_VAL; //Reset value on counter 
    
    //read value on bus
    for(f=0;f< (int)(CIRCLES_FOR_1MS * DEAD_TIME_CORRECTION * time); f++){
      for(i=0;i<8;i++){
        
        REG_PIOD_SODR = CLC_PIN_VAL; //send signal to clc, change is triggered on rinsing edge but time is needed for hardwere to set it's state
        REG_PIOD_CODR = CLC_PIN_VAL; //turn of clc
        
        val = (REG_PIOC_PDSR & pin_mask)>>1; //read value

        /*
        *   Dealing with counters overflow:
        *   table previousValue has value of last state
        *   If previous state is bigger calculate overflow 
        */

        if(previousValue[i] <= val){ 
            counts_pointer[i] += val - previousValue[i];
        }
        else{
            counts_pointer[i] += val + 16 - previousValue[i]; //15 is max for 4 bit counters but 16 gives value of 1 for 0 state  
        }

        previousValue[i]= val; 

      }

    
      REG_PIOD_SODR = CLC_PIN_VAL; //reset clc empty shift register circle 
      REG_PIOD_CODR = CLC_PIN_VAL;
    
    }

  }

  interrupts();
}

void write_output(){
  /**
   *  @brief print output to serial port 
   */
  SerialUSB.println(START_DATA);
  char printf_buffer[PRINTF_BUFFER_SIZE] = {0}; 
  for(int i=0;i<16;i++){
    sprintf(printf_buffer, "%dA%d\t%d\0",
            MULTIPLEXER_NR(i), (i-((MULTIPLEXER_NR(i)-1)*8))+1,
            counts[i]);
    SerialUSB.println(printf_buffer);
    clear_char_table(printf_buffer,PRINTF_BUFFER_SIZE);
    counts[i]=0;
  }
  
  SerialUSB.println(STOP_DATA);
  SerialUSB.flush();

}

void set_multiplexer(int state_to_set){
  /**
   * @brief Sets state of external multiplexer
   * @param state_to_set binary flag true for first multiplexed 8 false for secend
  */

  if(state_to_set){
    REG_PIOD_SODR = MULTIPLEXER_PIN_VAL; // set begining multiplexer state for HIGH.
  }
  else{
    REG_PIOD_CODR = MULTIPLEXER_PIN_VAL; // set begining multiplexer state for LOW.
  }

  multiplexer_state_flag = state_to_set;

}

void receive_command(){
  if(!command_in_buffer_flag){
    command_pointer = received_buffer;
  }

  while(SerialUSB.available() > 0)
  {
    command_in_buffer_flag = 1;
    *command_pointer = SerialUSB.read();
    SerialUSB.print(READY_TO_READ);

    command_pointer= received_buffer;
    while(!SerialUSB.available()); //wait for command

    while(command_in_buffer_flag){
      while (SerialUSB.available()>0){
        *command_pointer =  SerialUSB.read();
        if(*command_pointer == COMAND_ENDING_CONST){
          analyze_command();
        }
        command_pointer++;
      }
    }
  }

  if(SerialUSB.available()){
    receive_command();
  }
  SerialUSB.flush();
}

void analyze_command(){
  cut_ending();
  if(!strcmp(received_buffer, HANSHAKE_CONFIRM_REQUEST_CODE)){
    SerialUSB.print(HANSHAKE_CONFIRMATION_CODE);
    SerialUSB.print(COMAND_ENDING_CONST);
  }else{

  if(!strcmp( received_buffer, AKW_TIME_MS_CODE)){
    akw_time = read_number();
    SerialUSB.print( (int) akw_time);
    SerialUSB.print(COMAND_ENDING_CONST);
  }else{

  if(!strcmp( received_buffer, START_CODE)){
    hibernation_flag = false;
  }else{

  if(!strcmp( received_buffer, STOP_CODE)){
    SerialUSB.print(CODE_STOPED_RESPONSE);
    SerialUSB.print(COMAND_ENDING_CONST);
    hibernation_flag = true;
  }else{
    
    //unknown command
    SerialUSB.println("Don't understend");
    SerialUSB.print("Received:");
    SerialUSB.println(received_buffer);

  }}}} // :( 
  command_in_buffer_flag = 0;
}

int read_number(){
  char* command_pointer = received_buffer;
  while(!SerialUSB.available()); // wait for data

  int have_number_flag = false;

  while(!have_number_flag){
    while (SerialUSB.available() > 0){
      *command_pointer = SerialUSB.read();
      if(*command_pointer == COMAND_ENDING_CONST){
        have_number_flag = true;
      }
      command_pointer++;
    }
  }
  cut_ending();
  return atoi(received_buffer);
}

void cut_ending(){
  received_buffer[strlen(received_buffer)-1] = '\0';
}

void clear_char_table(char* table, int len){
  for(int i = 0; i<len; i++){
   *table = '\0';
    table++; 
  }
}

void clear_int_table(int* table, int len){
  for(int i = 0; i<len; i++){
   *table = 0;
    table++; 
  }
}