#include "uart.h"

// Register Structures
typedef struct {
    volatile uint32_t SR;
    volatile uint32_t DR;
    volatile uint32_t BRR;
    volatile uint32_t CR1;
    volatile uint32_t CR2;
    volatile uint32_t CR3;
    volatile uint32_t GTPR;
} USART_RegDef_t;

typedef struct {
    volatile uint32_t CR;
    volatile uint32_t NDTR;
    volatile uint32_t PAR;
    volatile uint32_t M0AR;
    volatile uint32_t M1AR;
    volatile uint32_t FCR;
} DMA_Stream_RegDef_t;

typedef struct {
    volatile uint32_t ISR[2];
    volatile uint32_t IFCR[2];
    DMA_Stream_RegDef_t Stream[8];
} DMA_RegDef_t;

// Base Addresses
#define USART2_BASE   (0x40004400UL)
#define DMA1_BASE     (0x40026000UL)
#define GPIOA_BASE    (0x40020000UL)
#define RCC_BASE      (0x40023800UL)

#define USART2        ((USART_RegDef_t *)USART2_BASE)
#define DMA1          ((DMA_RegDef_t *)DMA1_BASE)

#define RCC_AHB1ENR   (*(volatile uint32_t *)(RCC_BASE + 0x30UL))
#define RCC_APB1ENR   (*(volatile uint32_t *)(RCC_BASE + 0x40UL))

static volatile uint8_t dma_tx_busy = 0;

void UART2_Init(uint32_t baudrate) {
    // 1. Enable GPIOA, USART2, and DMA1 clocks
    RCC_AHB1ENR |= (1U << 0);  // GPIOA clock enable
    RCC_APB1ENR |= (1U << 17); // USART2 clock enable
    RCC_AHB1ENR |= (1U << 21); // DMA1 clock enable

    // 2. Configure PA2 (TX) as Alternate Function (AF7)
    volatile uint32_t *GPIOA_MODER = (volatile uint32_t *)(GPIOA_BASE + 0x00UL);
    volatile uint32_t *GPIOA_AFRL  = (volatile uint32_t *)(GPIOA_BASE + 0x20UL);
    
    *GPIOA_MODER &= ~(0x3U << (2 * 2));
    *GPIOA_MODER |=  (0x2U << (2 * 2)); // AF Mode
    *GPIOA_AFRL  &= ~(0xFU << (2 * 4));
    *GPIOA_AFRL  |=  (0x7U << (2 * 4)); // AF7 for USART2

    // 3. Configure USART2 Baud Rate (Assuming 16 MHz APB1 clock)
    // BRR = 16000000 / baudrate (For 115200 -> ~138.8 -> 0x8B)
    USART2->BRR = (16000000 + (baudrate / 2)) / baudrate;

    // 4. Enable Transmitter, DMA Transmitter, and USART2
    USART2->CR1 = (1U << 3);  // TE: Transmitter enable
    USART2->CR3 = (1U << 7);  // DMAT: DMA mode enable for transmission
    USART2->CR1 |= (1U << 13);// UE: USART enable

    // 5. Configure DMA1 Stream 6 (Channel 4 maps to USART2_TX)
    DMA1->Stream[6].CR &= ~(1U << 0); // Disable DMA Stream 6 before config
    while (DMA1->Stream[6].CR & (1U << 0)); // Wait for disable

    // Clear interrupt flags for Stream 6
    DMA1->IFCR[1] |= (0x3FU << 16);

    // Set Peripheral Address (USART2 Data Register)
    DMA1->Stream[6].PAR = (uint32_t)&(USART2->DR);

    // Configure Stream 6 Control Register:
    // - Channel 4 (CHSEL = 100)
    // - Memory-to-peripheral (DIR = 01)
    // - Memory increment mode (MINC = 1)
    // - Transfer complete interrupt enable (TCIE = 1)
    uint32_t cr_val = (4U << 25) | (1U << 6) | (1U << 10) | (1U << 4);
    DMA1->Stream[6].CR = cr_val;

    // Enable DMA1 Stream 6 interrupt in NVIC (IRQn 60 for DMA1_Stream6)
    volatile uint32_t *NVIC_ISER1 = (volatile uint32_t *)0xE000E104UL;
    *NVIC_ISER1 |= (1U << (60 - 32));
}

void UART2_SendBytes_DMA(uint8_t *data, uint16_t size) {
    while (dma_tx_busy); // Wait for previous transmission to complete

    dma_tx_busy = 1;

    // Disable stream, set memory address and size
    DMA1->Stream[6].CR &= ~(1U << 0);
    while (DMA1->Stream[6].CR & (1U << 0));

    DMA1->Stream[6].M0AR = (uint32_t)data;
    DMA1->Stream[6].NDTR = size;

    // Clear flags and enable stream
    DMA1->IFCR[1] |= (0x3FU << 16);
    DMA1->Stream[6].CR |= (1U << 0);
}

void UART2_SendString_DMA(const char *str) {
    uint16_t len = 0;
    while (str[len] != '\0') {
        len++;
    }
    UART2_SendBytes_DMA((uint8_t *)str, len);
}

uint8_t UART2_IsTxCompleted(void) {
    return !dma_tx_busy;
}

// DMA1 Stream 6 Interrupt Handler
void DMA1_Stream6_IRQHandler(void) {
    if (DMA1->ISR[1] & (1U << 21)) { // Check Transfer Complete Interrupt Flag
        DMA1->IFCR[1] |= (1U << 21); // Clear TCIF flag
        dma_tx_busy = 0;             // Mark transmission as complete
    }
}
