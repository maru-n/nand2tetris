// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.


(MAIN_LOOP)
    @i
    M=0
    @KBD
    D=M
    @FILL_BLACK
    D;JNE
    @FILL_WHITE
    0;JMP

(FILL_BLACK)
    @i
    D=M
    @SCREEN
    A=A+D
    M=-1
    @i
    M=M+1
    D=M
    @8192
    D=A-D
    @FILL_BLACK
    D;JGT
    @MAIN_LOOP
    0;JMP

(FILL_WHITE)
    @i
    D=M
    @SCREEN
    A=A+D
    M=0
    @i
    M=M+1
    D=M
    @8192
    D=A-D
    @FILL_WHITE
    D;JGT
    @MAIN_LOOP
    0;JMP
