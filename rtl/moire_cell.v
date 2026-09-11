// STUB / behavioral: Moiré excitonic cell (sync reset, active-high)
`timescale 1ns/1ps

module moire_cell #(
    parameter WIDTH = 1
) (
    input  wire clk,
    input  wire rst,
    input  wire [WIDTH-1:0] a,
    input  wire [WIDTH-1:0] b,
    output reg  [WIDTH-1:0] y_nand
);
    integer i;
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            y_nand <= {WIDTH{1'b0}};
        end else begin
            for (i = 0; i < WIDTH; i = i + 1)
                y_nand[i] <= ~(a[i] & b[i]);
        end
    end
endmodule
