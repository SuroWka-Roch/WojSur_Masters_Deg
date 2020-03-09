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
#define CHOOSE_MULTIPLEXER_CODE "cmx"
#define AKW_TIME_MS_CODE "atm"
#define START_CODE "srt"
#define STOP_CODE "stp"

#define START_DATA "<~+~>"
#define STOP_DATA "~<+>~"

//CONFIG
#define STARTING_MULTIPLEXER_STATE 0

//4.618us per circle 
#define CIRCLES_FOR_1MS (21656.0/100.0)
#define DEAD_TIME_CORRECTION (1.14503073835)

//pinout set up
//All output is done on periferal PC 
#define CLC_PIN_NUM 19 //Arduino pin 44
#define CLC_PIN_VAL 0x1<<CLC_PIN_NUM  //2^19

#define MULTIPLEXER_PIN_NUM 18 //Arduino pin 45
#define MULTIPLEXER_PIN_VAL 0x1<<MULTIPLEXER_PIN_NUM  

#define CLEAR_PIN_NUM 17 //Arduino pin 46
#define CLEAR_PIN_VAL 0x1<<CLEAR_PIN_NUM 

#endif 