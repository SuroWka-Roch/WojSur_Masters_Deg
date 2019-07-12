

#define SYSCLC *(volatile uint32_t *) 0x400E0610 // I can't find the clc makro - Register for perifrel clc control
#define LOAD *(volatile uint32_t *) 0xE000E014 // Register defining value that system procesor loads when restarted - gives timer of milisecunds WO max 16777215
#define CTRL *(volatile uint32_t *) 0xE000E018 // At 16 there is a flag wheter clc reached 0 here are adidional options. RW
#define RELOAD *(volatile uint32_t *) 0xE000E018 // Writing anything in this register sets it to 0 sets TIMER_FLAG to 0 so it loads LOAD value.
//#define PIOC_OWDR *(volatile uint32_t *) 0x400E12A4 // Protect lines from writes on PIOC_ODSR, kind of a mask.
//#define PIOC_ODSR *(volatile uint32_t *) 0x400E1238 // Cool write register writen value is put on IO line
#define COMMEND_MAX_SIZE 30
/**************************************************************************************/

//All output is done on periferal PC

#define RESET 0xFFFFFFFF
#define TIMER_FLAG (CTRL & (0B1<<0))
#define pins 0B111111<<2

enum commends_names {
  AKW,
  TMP,
  CNF,
  BAD_COMMEND
};

unsigned int counts;

void add(){
  counts++;  
}

int ACQUISITION_TIME_MS = 1000; //must be int

void setup() {
  Serial.begin(9600);
  //noInterrupts(); // nie pozwala na wysyłanie serialne
  counts = 0;
  pinMode(33, INPUT_PULLUP);
  
  
  //REG_PIOC_OER = pins; // enable output
  //REG_PIOC_PUDR = pins; // pull up disable
  //SYSCLC = 1 << 13; //PMC Peripheral Clock Enable Register 0, turn on a periferal clock
  //LOAD = ACQUISITION_TIME_MS; 
  //CTRL = 0B101;
  delay(1000);
}

int test = 0;

void loop() {
    char commend[COMMEND_MAX_SIZE]={0}; //bufor for commend resived from P
    char b;
    int a = 0;
    if (Serial.available() > 0) {
      while((b=Serial.read())!='\n'){
        commend[a]=b;
        Serial.println(b);
        a++;
      }
      commend[a]='\0';
      switch(get_commend_form_string(commend)){
        case AKW:
          AKW_fun(commend);
          break;
        case CNF:
          break;
        case TMP:
          break;
        case BAD_COMMEND:
          Serial.println("error parsing");
      }
    }
}

char* AKW_fun(char* commend){
  Serial.println("IN AKW_fun");
  int volatile dummy;
  ACQUISITION_TIME_MS = get_int_from_commend(commend);
  Serial.println(ACQUISITION_TIME_MS);

  noInterrupts();
  attachInterrupt(digitalPinToInterrupt(33), add, RISING);
  interrupts();
  long int time =millis();
  while(millis()-time<ACQUISITION_TIME_MS){
        dummy++;
  }
  detachInterrupt(digitalPinToInterrupt(33));

  Serial.println(counts);
} 

enum commends_names get_commend_form_string(char* commend){
  char commendBuffer[4];
  for(int a=0;a<3;a++){
    commendBuffer[a] = commend[a];
  }
  commendBuffer[3]='\0';
  if( strcmp( commendBuffer , "AKW") == 0){
    return AKW;
  }
  else{
    return BAD_COMMEND;
  }
}

int get_int_from_commend(char* commend){
  commend+=3;
  int i=0;
  char valueBufor[COMMEND_MAX_SIZE];
  Serial.println(commend);
  while(*commend != '\0'){
    valueBufor[i]=*commend;
    commend++;
    i++;
  }
  Serial.println(i);
  String temp  = (String) valueBufor; 
  return temp.toInt();
}
