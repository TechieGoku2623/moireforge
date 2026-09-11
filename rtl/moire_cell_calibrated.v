`timescale 1ns/1ps
// STUB / behavioral: calibrated delay / skew placeholders

module moire_cell_calibrated #(
    parameter SKEW_PS = 0
) (
    input  wire clk,
    input  wire rst,
    input  wire a,
    input  wire b,
    output wire y
);
    wire y_raw;
    moire_nand2 core (.a(a), .b(b), .y(y_raw));
    assign #(SKEW_PS) y = y_raw;
endmodule
