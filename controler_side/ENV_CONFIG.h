/**
 * @file ENV_CONFIG.h
 * @brief Header to set environment for arm/arduiono due microcontroler. 
 * 
*/

#ifndef ENV_CONFIG_DUE_MINE
#define ENV_CONFIG_DUE_MINE

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
void(* resetFunc) (void) = 0; //declare reset function at address 0

#define MULTIPLEXER_NR(canal_nr) ((((canal_nr)/8)%2)+1)
/**************************************************************************************/
#endif //end ENV_CONFIG