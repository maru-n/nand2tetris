#!/usr/bin/env python


class Code(object):

    """docstring for Code"""
    COMP_CODE_MAP = {
        '0':   0b0101010,
        '1':   0b0111111,
        '-1':  0b0111010,
        'D':   0b0001100,
        'A':   0b0110000,
        '!D':  0b0001101,
        '!A':  0b0110001,
        '-D':  0b0001111,
        '-A':  0b0110011,
        'D+1': 0b0011111,
        'A+1': 0b0110111,
        'D-1': 0b0001110,
        'A-1': 0b0110010,
        'D+A': 0b0000010,
        'D-A': 0b0010011,
        'A-D': 0b0000111,
        'D&A': 0b0000000,
        'D|A': 0b0010101,
        'M':   0b1110000,
        '!M':  0b1110001,
        'M+1': 0b1110111,
        'M-1': 0b1110010,
        'D+M': 0b1000010,
        'D-M': 0b1010011,
        'M-D': 0b1000111,
        'D&M': 0b1000000,
        'D|M': 0b1010101,
    }
    DEST_CODE_MAP = {
        'M':   0b001,
        'D':   0b010,
        'MD':  0b011,
        'A':   0b100,
        'AM':  0b101,
        'AD':  0b110,
        'AMD': 0b111,
        None:  0b000,
    }
    JUMP_CODE_MAP = {
        'JGT': 0b001,
        'JEQ': 0b010,
        'JGE': 0b011,
        'JLT': 0b100,
        'JNE': 0b101,
        'JLE': 0b110,
        'JMP': 0b111,
        None:  0b000,
    }

    def __init__(self):
        super(Code, self).__init__()

    @classmethod
    def dest(cls, mnemonic):
        return cls.DEST_CODE_MAP[mnemonic]

    @classmethod
    def comp(cls, mnemonic):
        return cls.COMP_CODE_MAP[mnemonic]

    @classmethod
    def jump(cls, mnemonic):
        return cls.JUMP_CODE_MAP[mnemonic]
