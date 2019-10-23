#include "include/sam.h"

#define ALL 0xFFFFFFFF

#ifndef __NO_SYSTEM_INIT
void SystemInit()
{
}
#endif



int flag = 0;

void dummy(void)
{
    ;
}

void delay()
{
    for (int i = 0; i < 1E10; i++)
    {
        dummy();
    }
}

void set_up(void){
    __set_CONTROL(0); //Enter privliged mode
    REG_PMC_WPMR = 0x504D4300; //disable write protection
    REG_PMC_PCER0 = REG_PMC_PCER0 || 1UL<<ID_PIOC; // Enable periferal clc
    REG_PIOC_PER = ALL;
    REG_PIOC_OER = ALL;
    REG_PIOC_SODR = PIO_CODR_P1;
}
void main()
{   
    set_up();
    /*
        for (;;){
            delay();
            REG_PIOC_SODR = ALL;
            delay();
            REG_PIOC_SODR = ALL;
        }
        */
    for (;;)
        ;
    dummy();
}
