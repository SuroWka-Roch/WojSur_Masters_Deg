

//#define SYSCLC *(volatile uint32_t *) 0x400E0610 // I can't find the clc makro - Register for perifrel clc control
#define LOAD *(volatile uint32_t *) 0xE000E014 // Register defining value that system procesor loads when restarted - gives timer of milisecunds WO max 16777215
#define CTRL *(volatile uint32_t *) 0xE000E018 // At 16 there is a flag wheter clc reached 0 here are adidional options. RW
#define RELOAD *(volatile uint32_t *) 0xE000E018 // Writing anything in this register sets it to 0 sets TIMER_FLAG to 0 so it loads LOAD value.
//#define PIOC_OWDR *(volatile uint32_t *) 0x400E12A4 // Protect lines from writes on PIOC_ODSR, kind of a mask.
//#define PIOC_ODSR *(volatile uint32_t *) 0x400E1238 // Cool write register writen value is put on IO line

/**************************************************************************************/

//All output is done on periferal PC


#define TIMER_FLAG CTRL & (0B1<<16)
#define pins 0B111111<<2

unsigned int counts;

void add(){
  counts++;  
}

int ACQUISITION_TIME_MS = 10000; //must be int
void setup() {
  Serial.begin(9600);

  /* Using pointers to table as a way to deal witch multiplexing with low procesor yeald */

  //noInterrupts();
  counts = 0;
  pinMode(33, INPUT_PULLUP);
  //attachInterrupt(digitalPinToInterrupt(33), add, RISING);
  
  //REG_PIOC_OER = pins; // enable output
  //REG_PIOC_PUDR = pins; // pull up disable
  //SYSCLC = 1 << 13; //PMC Peripheral Clock Enable Register 0, turn on a periferal clock
  LOAD = ACQUISITION_TIME_MS;
}

char string[30]={0};
long int a =0;
void loop() {
    flag=true;
    Serial.println("lol");
    delay(1000);
    char incomingByte = 0;
    if (Serial.available() > 0) {
      Serial.print("erp");
      delay(100);
      incomingByte = Serial.read();
      if (incomingByte == 'A')
      { 
        While(flag){
          if(Serial.available() > 0){
            incomingByte = Serial.read();
           }
        }
        int i=0;
        int b;
        while((b=Serial.read())!=-1){
          string[i]=b;

          i++;
        }
        string[i]= '\0';
        Serial.println(string);
        ACQUISITION_TIME_MS = String(string).toInt();
        LOAD = ACQUISITION_TIME_MS;
        Serial.println(ACQUISITION_TIME_MS);
        RELOAD = true; //start the clock TIMER_FLAG
        interrupts();
        while (!TIMER_FLAG) {
          
        a++;
        Serial.println(ACQUISITION_TIME_MS);
        }
        noInterrupts();
  
      }
  
    /*print output to serial port */
    
      Serial.println(counts);
    }

  
}
