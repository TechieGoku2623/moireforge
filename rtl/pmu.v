// Simple DVFS / clock enable PMU stub
`timescale 1ns/1ps

module pmu (
    input  wire clk,
    input  wire rst,
    input  wire [3:0] throttle,
    output reg  clk_gate_en
);
    always @(posedge clk or posedge rst) begin
        if (rst) clk_gate_en <= 1'b0;
        else clk_gate_en <= |throttle;
    end
endmodule
