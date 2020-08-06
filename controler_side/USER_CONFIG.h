#ifndef USER_CONFIG
#define USER_CONFIG

//communication constants
#define SERIAL_SPEED 9600
#define RECEIVED_BUFFER_SIZE 20
#define PRINTF_BUFFER_SIZE 15
#define COMAND_ENDING_CONST '\n'
#define READY_TO_READ "Ready to read\n"
#define HANSHAKE_CONFIRM_REQUEST_CODE "42a"
#define HANSHAKE_CONFIRMATION_CODE "42b"
#define CHOOSE_MULTIPLEXER_CODE "cmx" // absolute 
#define AKW_TIME_MS_CODE "atm"
#define START_CODE "srt"
#define STOP_CODE "stp"
#define CODE_STOPED_RESPONSE "fin"
#define LOW_RATE_CODE "lrt"
#define ENBLR_CODE "enr"

#define START_DATA "<~+~>"
#define STOP_DATA "~<+>~"

//CONFIG
#define STARTING_MULTIPLEXER_STATE 0

// //(184162.062615/1000.0) 5.43us    old value = 4.618us per circle  (21656.0/100.0); new val = 5.25us
#define CIRCLES_FOR_1MS  (221.238938053) // 4.52us
#define DEAD_TIME_CORRECTION (1.1370658292319538) // last one 1/0.88185  ///(1.31106274746)    //1/0.76274

//pinout set up
#ifdef N_D_per
#define CLC_PIN_NUM 19 //Arduino pin 44
#define CLC_PIN_VAL 0x1<<CLC_PIN_NUM  //2^19

#define MULTIPLEXER_PIN_NUM 18 //Arduino pin 45
#define MULTIPLEXER_PIN_VAL 0x1<<MULTIPLEXER_PIN_NUM  

#define CLEAR_PIN_NUM 17 //Arduino pin 46
#define CLEAR_PIN_VAL 0x1<<CLEAR_PIN_NUM 

#else

//All output is done on periferal PD

#define CLC_PIN_NUM 0 //Arduino pin 25
#define CLC_PIN_VAL 0x1<<CLC_PIN_NUM 

#define MULTIPLEXER_PIN_NUM 2 //Arduino pin 27
#define MULTIPLEXER_PIN_VAL 0x1<<MULTIPLEXER_PIN_NUM  

#define CLEAR_PIN_NUM 1 //Arduino pin 26
#define CLEAR_PIN_VAL 0x1<<CLEAR_PIN_NUM 

// Low Rate arduino pin 28 d3
#define LOW_RATE_PIN_NUM 3 
#define LOW_RATE_PIN_VAL 0x1<<LOW_RATE_PIN_NUM

//ENBLR arduino pin 30 D9
#define ENBLR_PIN_NUM 9
#define ENBLR_PIN_VAL 0x1<<ENBLR_PIN_NUM

#endif

#endif 