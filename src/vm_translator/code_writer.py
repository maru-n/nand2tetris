#!/usr/bin/env python

from os import path


class CodeWriter(object):

    def __init__(self, file_name):
        super(CodeWriter, self).__init__()
        self.set_file_name(file_name)
        self.__vmname = path.splitext(path.basename(file_name))[0]
        self.__global_line_symbol_index = 0

    def set_file_name(self, file_name):
        self.__file = open(file_name, 'w')

    def write_arithemetic(self, command):
        if command == 'add':
            self.__write_asm_pop_to_d_register()
            self.__write_asm_pop_to_a_register()
            self.__write_asm_code('D=D+A')
            self.__write_asm_push_from_d_register()
        elif command == 'sub':
            self.__write_asm_pop_to_d_register()
            self.__write_asm_pop_to_a_register()
            self.__write_asm_code('D=A-D')
            self.__write_asm_push_from_d_register()
        elif command == 'neg':
            self.__write_asm_pop_to_d_register()
            self.__write_asm_code('D=-D')
            self.__write_asm_push_from_d_register()
        elif command == 'eq':
            self.__write_asm_pop_to_d_register()
            self.__write_asm_pop_to_a_register()
            self.__write_asm_code('D=A-D')
            self.__write_asm_push_boolean_by_ifelse('D;JEQ')
        elif command == 'gt':
            self.__write_asm_pop_to_d_register()
            self.__write_asm_pop_to_a_register()
            self.__write_asm_code('D=A-D')
            self.__write_asm_push_boolean_by_ifelse('D;JGT')
        elif command == 'lt':
            self.__write_asm_pop_to_d_register()
            self.__write_asm_pop_to_a_register()
            self.__write_asm_code('D=A-D')
            self.__write_asm_push_boolean_by_ifelse('D;JLT')
        elif command == 'and':
            self.__write_asm_pop_to_d_register()
            self.__write_asm_pop_to_a_register()
            self.__write_asm_code('D=A&D')
            self.__write_asm_push_from_d_register()
        elif command == 'or':
            self.__write_asm_pop_to_d_register()
            self.__write_asm_pop_to_a_register()
            self.__write_asm_code('D=A|D')
            self.__write_asm_push_from_d_register()
        elif command == 'not':
            self.__write_asm_pop_to_d_register()
            self.__write_asm_code('D=!D')
            self.__write_asm_push_from_d_register()

    def write_push_pop(self, command, segment, index):
        if command == 'C_PUSH':
            if segment == 'constant':
                self.__write_asm_code('@' + index)
                self.__write_asm_code('D=A')
                self.__write_asm_push_from_d_register()
            elif segment == 'local':
                self.__write_asm_push_from_base_addr_register('LCL', index)
            elif segment == 'argument':
                self.__write_asm_push_from_base_addr_register('ARG', index)
            elif segment == 'this':
                self.__write_asm_push_from_base_addr_register('THIS', index)
            elif segment == 'that':
                self.__write_asm_push_from_base_addr_register('THAT', index)
            elif segment == 'temp':
                self.__write_asm_push_from_base_addr('5', index)
            elif segment == 'pointer':
                self.__write_asm_push_from_base_addr('3', index)
            elif segment == 'static':
                static_symbol = self.__vmname + '.' + str(index)
                self.__write_asm_code('@'+static_symbol)
                self.__write_asm_code('D=M')
                self.__write_asm_push_from_d_register()
        elif command == 'C_POP':
            if segment == 'local':
                self.__write_asm_pop_to_base_addr_register('LCL', index)
            elif segment == 'argument':
                self.__write_asm_pop_to_base_addr_register('ARG', index)
            elif segment == 'this':
                self.__write_asm_pop_to_base_addr_register('THIS', index)
            elif segment == 'that':
                self.__write_asm_pop_to_base_addr_register('THAT', index)
            elif segment == 'temp':
                self.__write_asm_pop_to_base_addr('5', index)
            elif segment == 'pointer':
                self.__write_asm_pop_to_base_addr('3', index)
            elif segment == 'static':
                static_symbol = self.__vmname + '.' + str(index)
                self.__write_asm_pop_to_d_register()
                self.__write_asm_code('@'+static_symbol)
                self.__write_asm_code('M=D')

    def __get_new_jmp_symbol(self):
        symbol = 'GLOBAL_SYMBOL_' + str(self.__global_line_symbol_index)
        self.__global_line_symbol_index += 1
        return symbol

    def __write_asm_push_from_base_addr_register(self,
                                                 base_addr_register,
                                                 index):
        self.__write_asm_code('@' + base_addr_register)
        self.__write_asm_code('D=M')
        self.__write_asm_code('@' + index)
        self.__write_asm_code('A=D+A')
        self.__write_asm_code('D=M')
        self.__write_asm_push_from_d_register()

    def __write_asm_pop_to_base_addr_register(self,
                                              base_addr_register,
                                              index):
        self.__write_asm_code('@' + base_addr_register)
        self.__write_asm_code('D=M')
        self.__write_asm_code('@' + index)
        self.__write_asm_code('D=D+A')
        self.__write_asm_code('@R13')
        self.__write_asm_code('M=D')
        self.__write_asm_pop_to_d_register()
        self.__write_asm_code('@R13')
        self.__write_asm_code('A=M')
        self.__write_asm_code('M=D')

    def __write_asm_push_from_base_addr(self, base_addr, index):
        self.__write_asm_code('@' + base_addr)
        self.__write_asm_code('D=A')
        self.__write_asm_code('@' + index)
        self.__write_asm_code('A=D+A')
        self.__write_asm_code('D=M')
        self.__write_asm_push_from_d_register()

    def __write_asm_pop_to_base_addr(self, base_addr, index):
        self.__write_asm_code('@' + base_addr)
        self.__write_asm_code('D=A')
        self.__write_asm_code('@' + index)
        self.__write_asm_code('D=D+A')
        self.__write_asm_code('@R13')
        self.__write_asm_code('M=D')
        self.__write_asm_pop_to_d_register()
        self.__write_asm_code('@R13')
        self.__write_asm_code('A=M')
        self.__write_asm_code('M=D')

    def __write_asm_push_boolean_by_ifelse(self, condition_asm_code):
        if_symbol = self.__get_new_jmp_symbol()
        end_symbol = self.__get_new_jmp_symbol()
        self.__write_asm_code('@' + if_symbol)
        self.__write_asm_code(condition_asm_code)
        self.__write_asm_code('D=0')
        self.__write_asm_code('@' + end_symbol)
        self.__write_asm_code('0;JMP')
        self.__write_asm_code('(' + if_symbol + ')')
        self.__write_asm_code('D=-1')
        self.__write_asm_code('@' + end_symbol)
        self.__write_asm_code('0;JMP')
        self.__write_asm_code('(' + end_symbol + ')')
        self.__write_asm_push_from_d_register()

    def __write_asm_pop_to_a_register(self):
        self.__write_asm_code('@SP')
        self.__write_asm_code('AM=M-1')
        self.__write_asm_code('A=M')

    def __write_asm_pop_to_d_register(self):
        self.__write_asm_code('@SP')
        self.__write_asm_code('AM=M-1')
        self.__write_asm_code('D=M')

    def __write_asm_push_from_d_register(self):
        self.__write_asm_code('@SP')
        self.__write_asm_code('A=M')
        self.__write_asm_code('M=D')
        self.__write_asm_code('@SP')
        self.__write_asm_code('M=M+1')

    def __write_asm_code(self, asm_code):
        self.__file.write(asm_code + '\n')

    def close(self):
        self.__file.close()
