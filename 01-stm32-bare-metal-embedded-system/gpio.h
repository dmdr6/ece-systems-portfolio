#ifndef GPIO_H
#define GPIO_H

#include <stdint.h>

#define GPIOA_BASE   (0x40020000UL)
#define GPIOB_BASE   (0x40020400UL)
#define GPIOC_BASE   (0x40020800UL)

typedef struct {
    volatile uint32_t MODER;
    volatile uint32_t OTYPER;
    volatile uint32_t OSPEEDR;
    volatile uint32_t PUPDR;
    volatile uint32_t IDR;
    volatile uint32_t ODR;
    volatile uint32_t BSRR;
    volatile uint32_t LCKR;
    volatile uint32_t AFR[2];
} GPIO_RegDef_t;

#define GPIOA ((GPIO_RegDef_t *)GPIOA_BASE)
#define GPIOB ((GPIO_RegDef_t *)GPIOB_BASE)
#define GPIOC ((GPIO_RegDef_t *)GPIOC_BASE)

typedef enum {
    GPIO_MODE_IN     = 0x0,
    GPIO_MODE_OUT    = 0x1,
    GPIO_MODE_ALT    = 0x2,
    GPIO_MODE_ANALOG = 0x3
} GPIO_Mode_t;

typedef enum {
    GPIO_PUPD_NONE = 0x0,
    GPIO_PUPD_PU   = 0x1,
    GPIO_PUPD_PD   = 0x2
} GPIO_PUPD_t;

void GPIO_Init(GPIO_RegDef_t *GPIOx, uint8_t pin, GPIO_Mode_t mode, GPIO_PUPD_t pupd);
void GPIO_WritePin(GPIO_RegDef_t *GPIOx, uint8_t pin, uint8_t state);
uint8_t GPIO_ReadPin(GPIO_RegDef_t *GPIOx, uint8_t pin);
void GPIO_TogglePin(GPIO_RegDef_t *GPIOx, uint8_t pin);

#endif
