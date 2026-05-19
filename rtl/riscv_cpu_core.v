// Minimal RV32I subset stub: fetch/decode placeholders for hierarchy tests
`timescale 1ns/1ps

module riscv_cpu_core (
    input  wire clk,
    input  wire rst,
    output reg  [31:0] i_addr,
    input  wire [31:0] i_data,
    output reg  [31:0] d_addr,
    output reg  [31:0] d_wdata,
    input  wire [31:0] d_rdata,
    output reg         d_we
);
    reg [31:0] pc;
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            pc <= 32'h8000_0000;
            i_addr <= 32'h8000_0000;
            d_addr <= 32'h0;
            d_wdata <= 32'h0;
            d_we <= 1'b0;
        end else begin
            pc <= pc + 4;
            i_addr <= pc;
            d_we <= 1'b0;
        end
    end
endmodule
