#include "timer.h"

#define RCC_BASE      (0x40023800UL)
#define RCC_APB1ENR   (*(volatile uint32_t *)(RCC_BASE + 0x40UL))

#define TIM2_BASE     (0x40000000UL)
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
} TIM_RegDef_t;

#define TIM2 ((TIM_RegDef_t *)TIM2_BASE)

static volatile uint32_t ms_ticks = 0;

void TIM2_Init_1ms(void) {
    // Enable TIM2 clock on APB1 bus
    RCC_APB1ENR |= (1U << 0);

    // Set prescaler for 1 MHz timer clock (assuming 16 MHz APB1 clock -> 16 / 16 = 1 MHz)
    TIM2->PSC = 16 - 1;
    
    // Set auto-reload for 1 ms interrupt (1 MHz / 1000 = 1 kHz)
    TIM2->ARR = 1000 - 1;

    // Enable Update Interrupt
    TIM2->DIER |= (1U << 0);

    // Enable TIM2 Counter
    TIM2->CR1 |= (1U << 0);

    // Enable TIM2 IRQ in NVIC (IRQn 28)
    volatile uint32_t *NVIC_ISER0 = (volatile uint32_t *)0xE000E100UL;
    *NVIC_ISER0 |= (1U << 28);
}

uint32_t millis(void) {
    return ms_ticks;
}

void delay_ms(uint32_t delay) {
    uint32_t start = millis();
    while ((millis() - start) < delay);
}

// ISR Handler for TIM2 Interrupt
void TIM2_IRQHandler(void) {
    if (TIM2->SR & (1U << 0)) {
        TIM2->SR &= ~(1U << 0); // Clear update interrupt flag
        ms_ticks++;
    }
}
