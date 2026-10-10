#ifndef TIMER_H
#define TIMER_H

#include <stdint.h>

void TIM2_Init_1ms(void);
uint32_t millis(void);
void delay_ms(uint32_t delay);

#endif
