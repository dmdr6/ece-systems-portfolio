#ifndef UART_H
#define UART_H

#include <stdint.h>

void UART2_Init(uint32_t baudrate);
void UART2_SendString_DMA(const char *str);
void UART2_SendBytes_DMA(uint8_t *data, uint16_t size);
uint8_t UART2_IsTxCompleted(void);

#endif
