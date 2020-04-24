#define SYSCLC *(volatile uint32_t *) 0x400E0610 // I can't find the clc makro - Register for perifrel clc control
#define LOAD *(volatile uint32_t *) 0xE000E014 // Register defining value that system procesor loads when restarted - gives timer of milisecunds WO max 16777215
//#define CTRL *(volatile uint32_t *) 0xE000E018 // At 16 there is a flag wheter clc reached 0 here are adidional options. Does not work for some random reason. IDK
#define RELOAD *(volatile uint32_t *) 0xE000E018 // Writing anything in this register sets it to 0 sets TIMER_FLAG to 0 so it loads LOAD value.
#define PIOC_OWDR *(volatile uint32_t *) 0x400E12A4 // Protect lines from writes on PIOC_ODSR, kind of a mask.
#define PIOC_ODSR *(volatile uint32_t *) 0x400E1238 // Cool write register writen value is put on IO line

/**************************************************************************************/

//All output is done on periferal PC

#define RESET 0xFFFFFFFF
#define TIMER_FLAG (CTRL & (0B1<<0))
#define pins 0B111111<<2 // from arduino pins 34 to 39
#define SEL_PINS 0B1111<<2 //Pins for selectring canal
#define PIN_TO_FLIP 0B1<<5 //multiplexer pin has fliped logic
#define COMMEND_MAX_SIZE 30
#define LowRate_ARDUINO_PIN_NUM 38
#define ENB2R_ARDUINO_PIN_NUM 39

/*
 * Comends structure is 3 leter command number without white space between and '\n' sybol.
 * Patern
 *  CCCII'\n'
 * Where:
 *  C - Comand name 
 *  I - Numeric value
 * Example:
 *  CNF01'\n'
 */


enum commends_names { 
  AKW,
  SEL,
  CNF,
  BAD_COMMEND
};

unsigned int counts; // read value max size of 4.294.967.296 - that's a lot
unsigned int ACQUISITION_TIME_MS; //must be int





void setup() {
  Serial.begin(9600);
  counts = 0;
  pinMode(33, INPUT_PULLUP);
  REG_PIOC_OER = pins; // Enable output for all pins but one.
  PIOC_OWDR = ~SEL_PINS; // mask pins from change while writing to PIOC_OWDR register
  //CODE
    //REG_PIOC_PUDR = pins; // pull up disable
    //SYSCLC = 1 << 13; //PMC Peripheral Clock Enable Register 0, turn on a periferal clock
    //LOAD = ACQUISITION_TIME_MS; 
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

int test = 0;

void loop() {
    char commend[COMMEND_MAX_SIZE]={0}; //bufor for commend resived from PC
    int b;
    int a = 0;
    if (Serial.available() > 0) {
      while((b=Serial.read())!='\n'){
        if(b!=-1){
          commend[a]=(char)b;
          a++;
          if(a>COMMEND_MAX_SIZE){
            Serial.println("Commend does not end with '\\n' or serial error.");
          }
        }
      }
      commend[a]='\0'; // add string ending to read data
      switch(get_commend_form_string(commend)){ //Choose action
        case AKW:
          AKW_fun(commend);
          break;
        case CNF:
          CNF_fun(commend);
          break;
        case SEL:
          SEL_fun(commend);
          break;
        case BAD_COMMEND: //default
          Serial.println("Error parsing"); 
      }
    }
}

void add(){
  counts++;  
}

void AKW_fun(char* commend){
  int volatile dummy; //needed to force compilator to not optymalize the while loop
  ACQUISITION_TIME_MS = get_int_from_commend(commend);
  noInterrupts(); // No interupts space for acurate timing
    attachInterrupt(digitalPinToInterrupt(33), add, RISING);
    long int time = millis();
  interrupts();

  while(millis()-time<ACQUISITION_TIME_MS){ //Time watchdog
        dummy++;
  }

  noInterrupts(); 
    detachInterrupt(digitalPinToInterrupt(33)); 
    // this function probably gonna add same time to counting thats why the usage  noInterupts space.
  interrupts();
  Serial.println(counts);
  counts=0;
} 

void SEL_fun(char* commend){
  int setUp = get_int_from_commend(commend);
  setUp = setUp<<2;
  setUp ^= PIN_TO_FLIP;
  PIOC_ODSR = setUp; // Shuld not blink values not changed. 
}


void CNF_fun(char* commend){//commend value is binary number <Commend><ENB2R><LowRate>
  int config = get_int_from_commend(commend);

  if (config>11){ //Error msg
    Serial.println("Commend too long");
    return;
  }
  
  /*
   * Silly way of cheacking whather this dec number reprezents bin value.
   * 5 is arbritary number
   * Lowrate is there in binary reprezentarion
   * and seting with simple arduino function no time requaierments.
   */

  int ENB2R = config>5 ? true:false;
  int LowRate = config%2 ? true:false;
  ENB2R ? digitalWrite(ENB2R_ARDUINO_PIN_NUM, HIGH):digitalWrite(ENB2R_ARDUINO_PIN_NUM, LOW); //set value for both 
  LowRate ? digitalWrite(LowRate_ARDUINO_PIN_NUM, HIGH):digitalWrite(LowRate_ARDUINO_PIN_NUM, LOW); 

}


enum commends_names get_commend_form_string(char* commend){ //Thats a bad code if i ever seen one.
  char commendBuffer[4]; //3 leter code buffer
  for(int a=0;a<3;a++){
    commendBuffer[a] = commend[a];
  }
  commendBuffer[3]='\0';
  if( strcmp( commendBuffer , "AKW") == 0){ //Shuld not cascade
    return AKW;
  }
  else{
    if(strcmp( commendBuffer , "CNF") == 0){
      return CNF;
    }
    else{
      if(strcmp( commendBuffer , "SEL") == 0){
        return SEL;
      }
      else{
        return BAD_COMMEND;
      }
    }
  }
}

int get_int_from_commend(char* commend){
  commend+=3; //place where numeric value starts
  int i=0;
  char valueBufor[COMMEND_MAX_SIZE];
  while(*commend != '\0'){
    valueBufor[i]=*commend;
    commend++;
    i++;
  }
  String temp  = (String) valueBufor; 
  return temp.toInt();
}