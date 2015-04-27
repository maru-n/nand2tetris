#!/usr/bin/env python

import sys
import glob
from os import path
from parser import Parser
from code_writer import CodeWriter


def parse_and_write(parser, code_writer):
    while parser.has_more_commands():
        parser.advance()

        if parser.command_type() == 'C_ARITHEMTIC':
            command = parser.arg1()
            code_writer.write_arithemetic(command)

        elif parser.command_type() == 'C_PUSH':
            segment = parser.arg1()
            index = parser.arg2()
            code_writer.write_push(segment, index)

        elif parser.command_type() == 'C_POP':
            segment = parser.arg1()
            index = parser.arg2()
            code_writer.write_pop(segment, index)

        elif parser.command_type() == 'C_LABEL':
            label = parser.arg1()
            code_writer.write_label(label)

        elif parser.command_type() == 'C_GOTO':
            label = parser.arg1()
            code_writer.write_goto(label)

        elif parser.command_type() == 'C_IF':
            label = parser.arg1()
            code_writer.write_if(label)

        elif parser.command_type() == 'C_FUNCTION':
            function_name = parser.arg1()
            num_locals = int(parser.arg2())
            code_writer.write_function(function_name, num_locals)

        elif parser.command_type() == 'C_RETURN':
            code_writer.write_return()

        elif parser.command_type() == 'C_CALL':
            function_name = parser.arg1()
            num_args = int(parser.arg2())
            code_writer.write_call(function_name, num_args)


if __name__ == '__main__':
    input_file = sys.argv[1]

    if path.isfile(input_file):
        src_files = [input_file]
        asm_file = path.splitext(input_file)[0] + ".asm"
    else:
        src_files = glob.glob(path.join(sys.argv[1], '*.vm'))
        asm_file = path.split(input_file.rstrip('/') + ".asm")[1]
        asm_file = path.join(input_file, asm_file)

    code_writer = CodeWriter(asm_file)

    if len(src_files) != 1:
        code_writer.write_init()

    for src_file in src_files:
        parser = Parser(src_file)
        parse_and_write(parser, code_writer)

    code_writer.close()
