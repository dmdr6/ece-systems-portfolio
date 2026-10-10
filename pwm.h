#ifndef PWM_H
#define PWM_H

#include <stdint.h>

void PWM_Init(void);
void PWM_SetDutyCycle(uint16_t duty);

#endif
