// STUB / behavioral: XY routing (64-bit flit)
`timescale 1ns/1ps

module noc_router #(
    parameter X = 0,
    parameter Y = 0,
    parameter W = 64
) (
    input  wire clk,
    input  wire rst,
    input  wire [W-1:0] in_n,
    input  wire [W-1:0] in_e,
    output reg  [W-1:0] out_local
);
    always @(posedge clk or posedge rst) begin
        if (rst) out_local <= {W{1'b0}};
        else out_local <= in_n ^ in_e ^ {{(W-16){1'b0}}, X[7:0], Y[7:0]};
    end
endmodule
