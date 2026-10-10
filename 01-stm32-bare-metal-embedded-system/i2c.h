#ifndef I2C_H
#define I2C_H

#include <stdint.h>

void I2C1_Init(void);
void I2C_WriteReg(uint8_t dev_addr, uint8_t reg_addr, uint8_t data);

#endif
