`timescale 1ns/1ps
// STUB / behavioral: gate-level smoke testbench

module tb_moire_gates;
    reg a, b;
    wire y_nand, y_nor, y_not;

    moire_nand2 u_nand (.a(a), .b(b), .y(y_nand));
    moire_nor2 u_nor   (.a(a), .b(b), .y(y_nor));
    moire_not u_not    (.a(a), .y(y_not));

    initial begin
        $dumpfile("moire_gates.vcd");
        $dumpvars(0, tb_moire_gates);
        a = 0; b = 0;
        #5 a = 0; b = 1;
        #5 a = 1; b = 0;
        #5 a = 1; b = 1;
        #5 $finish;
    end
endmodule
