/* Minimal RV32I bootloader stub — linker script places at ROM base */
.section .text.boot
.globl _start
_start:
    la sp, _stack_top
    call main
hang:
    j hang
