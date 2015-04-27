#!/usr/bin/env python

from os import path


class CodeWriter(object):

    def __init__(self, file_name):
        super(CodeWriter, self).__init__()
        self.__file = open(file_name, 'w')
        self.__global_line_symbol_index = 0

    def set_file_name(self, file_name):
        self.__class_name = path.splitext(path.basename(file_name))[0]
        self.__function_name = ""

    def close(self):
        self.__file.close()

    def write_init(self):
        self.__write_asm_value_assignment('SP', 256)
        self.write_call('Sys.init', 0)

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
            self.__write_asm_code('D=D&A')
            self.__write_asm_push_from_d_register()
        elif command == 'or':
            self.__write_asm_pop_to_d_register()
            self.__write_asm_pop_to_a_register()
            self.__write_asm_code('D=D|A')
            self.__write_asm_push_from_d_register()
        elif command == 'not':
            self.__write_asm_pop_to_d_register()
            self.__write_asm_code('D=!D')
            self.__write_asm_push_from_d_register()

    def write_push(self, segment, index):
        if segment == 'constant':
            self.__write_asm_code('@' + index)
            self.__write_asm_code('D=A')
            self.__write_asm_push_from_d_register()
            return

        if segment in ['local', 'argument', 'this', 'that', 'temp', 'pointer']:
            if segment == 'local':
                self.__write_asm_code('@LCL')
                self.__write_asm_code('D=M')
            elif segment == 'argument':
                self.__write_asm_code('@ARG')
                self.__write_asm_code('D=M')
            elif segment == 'this':
                self.__write_asm_code('@THIS')
                self.__write_asm_code('D=M')
            elif segment == 'that':
                self.__write_asm_code('@THAT')
                self.__write_asm_code('D=M')
            elif segment == 'temp':
                self.__write_asm_code('@5')
                self.__write_asm_code('D=A')
            elif segment == 'pointer':
                self.__write_asm_code('@3')
                self.__write_asm_code('D=A')
            self.__write_asm_code('@' + index)
            self.__write_asm_code('A=D+A')
            self.__write_asm_code('D=M')
            self.__write_asm_push_from_d_register()
            return

        if segment == 'static':
            static_symbol = self.__class_name + '.' + str(index)
            self.__write_asm_code('@'+static_symbol)
            self.__write_asm_code('D=M')
            self.__write_asm_push_from_d_register()
            return

    def write_pop(self, segment, index):
        if segment in ['local', 'argument', 'this', 'that', 'temp', 'pointer']:
            if segment == 'local':
                self.__write_asm_code('@LCL')
                self.__write_asm_code('D=M')
            elif segment == 'argument':
                self.__write_asm_code('@ARG')
                self.__write_asm_code('D=M')
            elif segment == 'this':
                self.__write_asm_code('@THIS')
                self.__write_asm_code('D=M')
            elif segment == 'that':
                self.__write_asm_code('@THAT')
                self.__write_asm_code('D=M')
            elif segment == 'temp':
                self.__write_asm_code('@5')
                self.__write_asm_code('D=A')
            elif segment == 'pointer':
                self.__write_asm_code('@3')
                self.__write_asm_code('D=A')
            self.__write_asm_code('@' + index)
            self.__write_asm_code('D=D+A')
            self.__write_asm_code('@R13')
            self.__write_asm_code('M=D')
            self.__write_asm_pop_to_d_register()
            self.__write_asm_code('@R13')
            self.__write_asm_code('A=M')
            self.__write_asm_code('M=D')
            return

        if segment == 'static':
            static_symbol = self.__class_name + '.' + str(index)
            self.__write_asm_pop_to_d_register()
            self.__write_asm_code('@'+static_symbol)
            self.__write_asm_code('M=D')
            return

    def write_label(self, label):
        self.__write_asm_label(self.__get_function_inner_label(label))

    def write_goto(self, label):
        self.__write_asm_code('@' + self.__get_function_inner_label(label))
        self.__write_asm_code('0;JMP')

    def write_if(self, label):
        self.__write_asm_pop_to_d_register()
        self.__write_asm_code('@' + self.__get_function_inner_label(label))
        self.__write_asm_code('D;JNE')

    def write_call(self, function_name, num_args):
        return_address = self.__get_new_jmp_symbol()
        self.__write_asm_code('@' + return_address)
        self.__write_asm_code('D=A')
        self.__write_asm_push_from_d_register()  # push return-address
        self.__write_asm_push_from_symbol('LCL')
        self.__write_asm_push_from_symbol('ARG')
        self.__write_asm_push_from_symbol('THIS')
        self.__write_asm_push_from_symbol('THAT')
        self.__write_asm_push_from_symbol('SP')
        self.write_push('constant', str(num_args))
        self.write_arithemetic('sub')
        self.write_push('constant', '5')
        self.write_arithemetic('sub')
        self.__write_asm_pop_to_symbol('ARG')
        self.__write_asm_symbol_assignment('LCL', 'SP')
        self.__write_asm_code('@' + function_name)
        self.__write_asm_code('0;JMP')
        self.__write_asm_label(return_address)

    def write_return(self):
        self.__write_asm_pop_to_symbol('R13')  # return value
        self.__write_asm_symbol_assignment('R14', 'ARG')  # return SP point
        self.__write_asm_symbol_assignment('SP', 'LCL')
        self.__write_asm_pop_to_symbol('THAT')
        self.__write_asm_pop_to_symbol('THIS')
        self.__write_asm_pop_to_symbol('ARG')
        self.__write_asm_pop_to_symbol('LCL')
        self.__write_asm_pop_to_symbol('R15')  # return address
        self.__write_asm_symbol_assignment('SP', 'R14')
        self.__write_asm_push_from_symbol('R13')
        self.__write_asm_code('@R15')
        self.__write_asm_code('A=M')
        self.__write_asm_code('0;JMP')

    def write_function(self, function_name, num_locals):
        self.__function_name = function_name
        self.__write_asm_label(function_name)
        for i in range(num_locals):
            self.write_push('constant', '0')

    def __get_function_inner_label(self, label):
        return self.__function_name + '$' + label

    def __write_asm_symbol_assignment(self, dst_symbol, src_target):
        self.__write_asm_code('@' + src_target)
        self.__write_asm_code('D=M')
        self.__write_asm_code('@' + dst_symbol)
        self.__write_asm_code('M=D')

    def __write_asm_value_assignment(self, dst_symbol, value):
        self.__write_asm_code('@' + str(value))
        self.__write_asm_code('D=A')
        self.__write_asm_code('@' + dst_symbol)
        self.__write_asm_code('M=D')

    def __get_new_jmp_symbol(self):
        symbol = 'GLOBAL_SYMBOL_' + str(self.__global_line_symbol_index)
        self.__global_line_symbol_index += 1
        return symbol

    def __write_asm_push_boolean_by_ifelse(self, condition_asm_code):
        if_symbol = self.__get_new_jmp_symbol()
        end_symbol = self.__get_new_jmp_symbol()
        self.__write_asm_code('@' + if_symbol)
        self.__write_asm_code(condition_asm_code)
        self.__write_asm_code('D=0')
        self.__write_asm_code('@' + end_symbol)
        self.__write_asm_code('0;JMP')
        self.__write_asm_label(if_symbol)
        self.__write_asm_code('D=-1')
        self.__write_asm_code('@' + end_symbol)
        self.__write_asm_code('0;JMP')
        self.__write_asm_label(end_symbol)
        self.__write_asm_push_from_d_register()

    def __write_asm_push_from_symbol(self, symbol):
        self.__write_asm_code('@' + symbol)
        self.__write_asm_code('D=M')
        self.__write_asm_push_from_d_register()

    def __write_asm_push_from_d_register(self):
        self.__write_asm_code('@SP')
        self.__write_asm_code('A=M')
        self.__write_asm_code('M=D')
        self.__write_asm_code('@SP')
        self.__write_asm_code('M=M+1')

    def __write_asm_pop_to_symbol(self, symbol):
        self.__write_asm_pop_to_d_register()
        self.__write_asm_code('@' + symbol)
        self.__write_asm_code('M=D')

    def __write_asm_pop_to_a_register(self):
        self.__write_asm_code('@SP')
        self.__write_asm_code('AM=M-1')
        self.__write_asm_code('A=M')

    def __write_asm_pop_to_d_register(self):
        self.__write_asm_code('@SP')
        self.__write_asm_code('AM=M-1')
        self.__write_asm_code('D=M')

    def __write_asm_label(self, label):
        self.__write_asm_code('(' + label + ')')

    def __write_asm_code(self, asm_code):
        self.__file.write(asm_code + '\n')
