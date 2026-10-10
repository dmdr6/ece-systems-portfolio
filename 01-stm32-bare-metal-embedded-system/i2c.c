#include "i2c.h"

#define I2C1_BASE     (0x40005400UL)
typedef struct {
    volatile uint32_t CR1;
    volatile uint32_t CR2;
    volatile uint32_t OAR1;
    volatile uint32_t OAR2;
    volatile uint32_t DR;
    volatile uint32_t SR1;
    volatile uint32_t SR2;
    volatile uint32_t CCR;
    volatile uint32_t TRISE;
} I2C_RegDef_t;

#define I2C1 ((I2C_RegDef_t *)I2C1_BASE)
#define RCC_AHB1ENR   (*(volatile uint32_t *)(0x40023830UL))
#define RCC_APB1ENR   (*(volatile uint32_t *)(0x40023840UL))

void I2C1_Init(void) {
    // Enable GPIOB and I2C1 clocks
    RCC_AHB1ENR |= (1U << 1); 
    RCC_APB1ENR |= (1U << 21);

    // Reset and initialize I2C1
    I2C1->CR1 = (1U << 15); 
    I2C1->CR1 &= ~(1U << 15);

    I2C1->CR2 = 16;         // Peripheral clock frequency = 16 MHz
    I2C1->CCR = 80;         // Standard Mode 100 kHz (16000000 / (2 * 100000))
    I2C1->TRISE = 17;       // Maximum rise time
    I2C1->CR1 |= (1U << 0); // Enable peripheral
}

void I2C_WriteReg(uint8_t dev_addr, uint8_t reg_addr, uint8_t data) {
    // Generate START condition
    I2C1->CR1 |= (1U << 8);
    while (!(I2C1->SR1 & (1U << 0))); // Wait for SB (Start Bit Generated)

    // Send Slave Address with Write flag (bit 0 = 0)
    I2C1->DR = (dev_addr << 1);
    while (!(I2C1->SR1 & (1U << 1))); // Wait for ADDR flag
    (void)I2C1->SR2;                  // Clear ADDR flag

    // Transmit Register Address
    I2C1->DR = reg_addr;
    while (!(I2C1->SR1 & (1U << 7))); // Wait for TXE (Transmit Data Register Empty)

    // Transmit Data Byte
    I2C1->DR = data;
    while (!(I2C1->SR1 & (1U << 7))); // Wait for TXE
    while (!(I2C1->SR1 & (1U << 2))); // Wait for BTF (Byte Transfer Finished)

    // Generate STOP condition
    I2C1->CR1 |= (1U << 9);
}
