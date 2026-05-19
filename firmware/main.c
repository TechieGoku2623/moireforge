/* Moiré SoC firmware entry — stubs for drivers */
#include <stdint.h>

volatile uint32_t* const TILE_CFG = (uint32_t*)0x40000000;

int main(void) {
    *TILE_CFG = 1u;
    return 0;
}
