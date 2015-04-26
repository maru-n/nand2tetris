#!/usr/bin/env python

from os import path
import sys
from parser import Parser
from code import Code
from symbol_table import SymbolTable

if __name__ == '__main__':
    asm_fname = sys.argv[1]
    hack_fname = path.splitext(asm_fname)[0] + ".hack"
    hack_file = open(hack_fname, 'w')

    symbol_table = SymbolTable()
    symbol_table.add_entry('SP', 0)
    symbol_table.add_entry('LCL', 1)
    symbol_table.add_entry('ARG', 2)
    symbol_table.add_entry('THIS', 3)
    symbol_table.add_entry('THAT', 4)
    for i in range(16):
        symbol_table.add_entry('R'+str(i), i)
    symbol_table.add_entry('SCREEN', 16384)
    symbol_table.add_entry('KBD', 24576)

    parser = Parser(asm_fname)

    line_address = 0
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == 'L_COMMAND':
            symbol = parser.symbol()
            address = line_address
            symbol_table.add_entry(symbol, address)
        else:
            line_address += 1

    parser.seek_head()
    var_address = 16
    while parser.has_more_commands():
        parser.advance()

        if parser.command_type() == 'L_COMMAND':
            continue

        elif parser.command_type() == 'A_COMMAND':
            symbol = parser.symbol()
            if symbol.isdigit():
                address = int(symbol)
            elif symbol_table.contains(symbol):
                address = symbol_table.get_address(symbol)
            else:
                address = var_address
                symbol_table.add_entry(symbol, address)
                var_address += 1
            machine_code = address

        elif parser.command_type() == 'C_COMMAND':
            comp = Code.comp(parser.comp())
            dest = Code.dest(parser.dest())
            jump = Code.jump(parser.jump())
            machine_code = 0b111 << 13 | comp << 6 | dest << 3 | jump

        machine_code_str = "{0:016b}".format(machine_code)
        hack_file.write(machine_code_str + '\n')
