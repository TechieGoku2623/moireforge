`timescale 1ns/1ps

module moire_nand2 (
    input  wire a,
    input  wire b,
    output wire y
);
    assign y = ~(a & b);
endmodule

module moire_nor2 (
    input  wire a,
    input  wire b,
    output wire y
);
    assign y = ~(a | b);
endmodule

module moire_not (
    input  wire a,
    output wire y
);
    assign y = ~a;
endmodule
