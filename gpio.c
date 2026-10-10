#include "gpio.h"

void GPIO_Init(GPIO_RegDef_t *GPIOx, uint8_t pin, GPIO_Mode_t mode, GPIO_PUPD_t pupd) {
    // Configure Mode (2 bits per pin)
    GPIOx->MODER &= ~(0x3U << (pin * 2));
    GPIOx->MODER |=  ((mode & 0x3U) << (pin * 2));

    // Configure Pull-up/Pull-down (2 bits per pin)
    GPIOx->PUPDR &= ~(0x3U << (pin * 2));
    GPIOx->PUPDR |=  ((pupd & 0x3U) << (pin * 2));
}

void GPIO_WritePin(GPIO_RegDef_t *GPIOx, uint8_t pin, uint8_t state) {
    if (state) {
        GPIOx->BSRR = (1U << pin);         // Set pin
    } else {
        GPIOx->BSRR = (1U << (pin + 16));  // Reset pin
    }
}

uint8_t GPIO_ReadPin(GPIO_RegDef_t *GPIOx, uint8_t pin) {
    return (uint8_t)((GPIOx->IDR >> pin) & 0x1U);
}

void GPIO_TogglePin(GPIO_RegDef_t *GPIOx, uint8_t pin) {
    GPIOx->ODR ^= (1U << pin);
}
