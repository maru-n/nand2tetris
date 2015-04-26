#!/usr/bin/env python

import sys
from os import path
from parser import Parser
from code_writer import CodeWriter

if __name__ == '__main__':
    src_fname = sys.argv[1]
    asm_fname = path.splitext(src_fname)[0] + ".asm"

    parser = Parser(src_fname)
    code_writer = CodeWriter(asm_fname)

    while parser.has_more_commands():
        parser.advance()
        #print '#' + parser.current_line
        if parser.command_type() == 'C_ARITHEMTIC':
            command = parser.arg1()
            code_writer.write_arithemetic(command)
        elif parser.command_type() in ['C_PUSH', 'C_POP']:
            command = parser.command_type()
            segment = parser.arg1()
            index = parser.arg2()
            code_writer.write_push_pop(command, segment, index)
        elif parser.command_type() == 'C_LABEL':
            label = parser.arg1()
            code_writer.write_label(label)
        elif parser.command_type() == 'C_GOTO':
            label = parser.arg1()
            code_writer.write_goto(label)
        elif parser.command_type() == 'C_IF':
            label = parser.arg1()
            code_writer.write_if(label)

    code_writer.close()
