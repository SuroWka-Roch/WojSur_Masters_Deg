#include "include/sam.h"
#include "include/system_sam3xa.h"

#define ALL 0xFFFFFFFF

#if false
#ifndef __NO_SYSTEM_INIT
void SystemInit()
{
}
#endif
#endif
int flag = 0;

void dummy(void)
{
    __NOP();
}

void delay()
{
    for (int i = 0; i < 1E10; i++)
    {
        dummy();
    }
}

void set_up(void)
{
    SystemInit();
    __set_CONTROL(0);          //Enter privliged mode
    REG_PMC_WPMR = 0x504D4300; //disable write protection


    REG_PMC_PCER0 = REG_PMC_PCER0 || 0x1u << ID_PIOC; // Enable periferal clc
    REG_PIOC_PER = ALL;
    REG_PIOC_OER = ALL;

    REG_PMC_PCER0 = REG_PMC_PCER0 || 0x1u << ID_PIOB; // Enable periferal clc
    REG_PIOB_PER = REG_PIOB_PER || PIO_SODR_P27;
    REG_PIOB_OER = REG_PIOB_OER || PIO_SODR_P27;
}
void main()
{   
    set_up();
    REG_PIOC_SODR = ALL;
    REG_PIOB_SODR = REG_PIOB_SODR || PIO_SODR_P27;
    for (;;)
        ;
    dummy();
}
