// SoC top-level stub tying CPU stub to a single accelerator tile
`timescale 1ns/1ps

module soc_top (
    input wire clk,
    input wire rst
);
    wire [63:0] ni, so;
    reg [7:0] cfg;
    wire [31:0] i_addr, d_addr, d_wdata;
    wire d_we;

    assign ni = 64'hA5A5_5A5A_1234_5678;

    riscv_cpu_core cpu (
        .clk(clk),
        .rst(rst),
        .i_addr(i_addr),
        .i_data(32'h0000_0013), // NOP-ish
        .d_addr(d_addr),
        .d_wdata(d_wdata),
        .d_rdata(32'h0),
        .d_we(d_we)
    );

    moire_accel_tile #(.TILE_ID(0)) accel (
        .clk(clk),
        .rst(rst),
        .tile_cfg(cfg),
        .north_in(ni),
        .south_out(so),
        .irq()
    );

    always @(posedge clk or posedge rst) begin
        if (rst) cfg <= 8'h01;
    end
endmodule
