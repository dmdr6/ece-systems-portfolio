#include "pwm.h"

#define TIM3_BASE     (0x40000400UL)
typedef struct {
    volatile uint32_t CR1;
    volatile uint32_t CR2;
    volatile uint32_t SMCR;
    volatile uint32_t DIER;
    volatile uint32_t SR;
    volatile uint32_t EGR;
    volatile uint32_t CCMR1;
    volatile uint32_t CCMR2;
    volatile uint32_t CCER;
    volatile uint32_t CNT;
    volatile uint32_t PSC;
    volatile uint32_t ARR;
} TIM3_RegDef_t;

#define TIM3 ((TIM3_RegDef_t *)TIM3_BASE)
#define RCC_APB1ENR   (*(volatile uint32_t *)(0x40023840UL))

void PWM_Init(void) {
    // Enable TIM3 clock
    RCC_APB1ENR |= (1U << 1);

    // Set Prescaler for 1 MHz timer clock (16 MHz / 16 = 1 MHz)
    TIM3->PSC = 16 - 1;

    // Set Auto-Reload Register for a 20 kHz PWM frequency (1 MHz / 20 kHz = 50 steps)
    TIM3->ARR = 50 - 1;

    // Configure Channel 1 as PWM Mode 1 (OC1M = 110) with preload enabled
    TIM3->CCMR1 &= ~(0xFFU);
    TIM3->CCMR1 |= (6U << 4); 
    TIM3->CCMR1 |= (1U << 3); 

    // Enable Channel 1 Output
    TIM3->CCER |= (1U << 0);

    // Set initial duty cycle to 0 (CCR1 register offset is 0x34)
    volatile uint32_t *CCR1 = (volatile uint32_t *)((uint32_t)TIM3 + 0x34);
    *CCR1 = 0;

    // Enable Timer Counter
    TIM3->CR1 |= (1U << 0);
}

void PWM_SetDutyCycle(uint16_t duty) {
    volatile uint32_t *CCR1 = (volatile uint32_t *)((uint32_t)TIM3 + 0x34);
    if (duty > 50) duty = 50; // Cap at max ARR period steps
    *CCR1 = duty;
}
