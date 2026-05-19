// Moiré accelerator tile — lightweight stub for hierarchy
`timescale 1ns/1ps

module moire_accel_tile #(
    parameter TILE_ID = 0,
    parameter W_DATA = 64
) (
    input  wire clk,
    input  wire rst,
    input  wire [7:0] tile_cfg,
    input  wire [W_DATA-1:0] north_in,
    output reg  [W_DATA-1:0] south_out,
    output reg  irq
);
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            south_out <= {W_DATA{1'b0}};
            irq <= 1'b0;
        end else begin
            south_out <= north_in ^ {{(W_DATA-8){1'b0}}, tile_cfg};
            irq <= ^north_in[7:0];
        end
    end
endmodule
