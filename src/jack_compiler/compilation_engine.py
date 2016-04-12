#!/usr/bin/env python

from symbol_table import SymbolTable
from vm_writer import VMWriter
import os

class CompilationEngine(object):

    WRITE_METADATA = False  # for symbol table test on chapter 11

    def __init__(self, tokenizer, symbol_table=None, vm_writer=None):
        super(CompilationEngine, self).__init__()
        self.tokenizer = tokenizer
        self.symbol_table = symbol_table if symbol_table else SymbolTable()
        self.vm_writer = vm_writer if vm_writer else VMWriter(open(os.devnull,"w"))
        self.__analysis_output = open(os.devnull,"w")


    def compile(self):
        self.run()


    def analysis(self, output):
        self.__analysis_output = output
        self.run()


    def run(self):
        if not self.tokenizer.has_more_tokens():
            raise Exception('Invalid EOF.')
        self.tokenizer.advance()
        self.__compile_class()


    """ Compile Program """
    def __compile_class(self):
        self.__analysis_output.write('<class>\n')
        self.__get_and_advance_token('class')
        self.__class_name = self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="class/defined")
        self.__get_and_advance_token('{')
        while self.tokenizer.get_current_token() in ['static', 'field']:
            self.__compile_class_var_dec()
        while self.tokenizer.get_current_token() in ['constructor', 'function', 'method']:
            self.__compile_subroutine_dec()
        self.__get_and_advance_token('}')
        self.__analysis_output.write('</class>\n')


    def __compile_class_var_dec(self):
        self.__analysis_output.write('<classVarDec>\n')
        var_kind = self.__get_and_advance_token(['static', 'field'])
        var_type = self.__get_token_as_var_type()
        var_name = self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata=var_kind+"/defined")
        self.symbol_table.define(var_name, var_type, var_kind)
        while self.tokenizer.get_current_token() == ',':
            self.__get_and_advance_token(',')
            var_name = self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata=var_kind+"/defined")
            self.symbol_table.define(var_name, var_type, var_kind)
        self.__get_and_advance_token(';')
        self.__analysis_output.write('</classVarDec>\n')


    def __compile_subroutine_dec(self):
        self.__analysis_output.write('<subroutineDec>\n')
        func_type = self.__get_and_advance_token(['constructor', 'function', 'method'])
        if self.tokenizer.get_current_token() == 'void':
            self.__get_and_advance_token('void')
        else:
            self.__get_token_as_var_type()
        func_name = self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="subroutine/defined")
        self.__get_and_advance_token('(')
        param_num = self.__compile_parameter_list()
        self.__get_and_advance_token(')')
        self.vm_writer.write_function(self.__class_name+'.'+func_name, param_num)
        self.__compile_subroutine_body()
        self.__analysis_output.write('</subroutineDec>\n')


    def __compile_parameter_list(self):
        self.__analysis_output.write('<parameterList>\n')
        param_cnt = 0
        if self.tokenizer.get_current_token() != ')':
            var_type = self.__get_token_as_var_type()
            var_name = self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="argument/defined")
            self.symbol_table.define(var_name, var_type, 'ARG')
            param_cnt = 0
            while self.tokenizer.get_current_token() == ',':
                self.__get_and_advance_token(',')
                var_type = self.__get_token_as_var_type()
                var_name = self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="argument/defined")
                self.symbol_table.define(var_name, var_type, 'ARG')
                param_cnt += 1
        self.__analysis_output.write('</parameterList>\n')
        return param_cnt



    def __compile_subroutine_body(self):
        self.__analysis_output.write('<subroutineBody>\n')
        self.__get_and_advance_token('{')
        while self.tokenizer.get_current_token() == 'var':
            self.__compile_var_dec()
        self.__compile_statements()
        self.__get_and_advance_token('}')
        self.__analysis_output.write('</subroutineBody>\n')


    def __compile_var_dec(self):
        self.__analysis_output.write('<varDec>\n')
        self.__get_and_advance_token('var')
        self.__get_token_as_var_type()
        var_name = self.__get_and_advance_token(valid_token_type="IDENTIFIER", metadata="var/defined")
        #self.symbol_table.define(var_name, var_type, 'ARG')
        while self.tokenizer.get_current_token() == ',':
            self.__get_and_advance_token(',')
            var_name = self.__get_and_advance_token(valid_token_type="IDENTIFIER", metadata="var/defined")
            #self.symbol_table.define(var_name, var_type, 'ARG')
        self.__get_and_advance_token(';')
        self.__analysis_output.write('</varDec>\n')


    def __get_token_as_var_type(self):
        try:
            var_type = self.__get_and_advance_token(['int', 'char', 'boolean'])
        except:
            var_type = self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="class/use")
        return var_type


    """ Compile Statement """
    def __compile_statements(self):
        self.__analysis_output.write('<statements>\n')
        while self.tokenizer.get_current_token() in ['let', 'if', 'while', 'do', 'return']:
            if self.tokenizer.get_current_token() == 'let':
                self.__compile_let_statement()
            elif self.tokenizer.get_current_token() == 'if':
                self.__compile_if_statement()
            elif self.tokenizer.get_current_token() == 'while':
                self.__compile_while_statement()
            elif self.tokenizer.get_current_token() == 'do':
                self.__compile_do_statement()
            elif self.tokenizer.get_current_token() == 'return':
                self.__compile_return_statement()
        self.__analysis_output.write('</statements>\n')


    def __compile_let_statement(self):
        self.__analysis_output.write('<letStatement>\n')
        self.__get_and_advance_token('let')
        self.__get_and_advance_token(valid_token_type='IDENTIFIER')
        if self.tokenizer.get_current_token() == '[':
            self.__get_and_advance_token('[')
            self.__compile_expression()
            self.__get_and_advance_token(']')
        self.__get_and_advance_token('=')
        self.__compile_expression()
        self.__get_and_advance_token(';')
        self.__analysis_output.write('</letStatement>\n')


    def __compile_if_statement(self):
        self.__analysis_output.write('<ifStatement>\n')
        self.__get_and_advance_token('if')
        self.__get_and_advance_token('(')
        self.__compile_expression()
        self.__get_and_advance_token(')')
        self.__get_and_advance_token('{')
        self.__compile_statements()
        self.__get_and_advance_token('}')
        if self.tokenizer.get_current_token() == 'else':
            self.__get_and_advance_token('else')
            self.__get_and_advance_token('{')
            self.__compile_statements()
            self.__get_and_advance_token('}')
        self.__analysis_output.write('</ifStatement>\n')


    def __compile_while_statement(self):
        self.__analysis_output.write('<whileStatement>\n')
        self.__get_and_advance_token('while')
        self.__get_and_advance_token('(')
        self.__compile_expression()
        self.__get_and_advance_token(')')
        self.__get_and_advance_token('{')
        self.__compile_statements()
        self.__get_and_advance_token('}')
        self.__analysis_output.write('</whileStatement>\n')


    def __compile_do_statement(self):
        self.__analysis_output.write('<doStatement>\n')
        self.__get_and_advance_token('do')
        subroutine_name = ""
        if self.tokenizer.get_next_token() == ".":
            subroutine_name += self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="class/use")
            subroutine_name += self.__get_and_advance_token('.')
        subroutine_name += self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="subroutine/use")
        self.__get_and_advance_token('(')
        n_args = self.__compile_expression_list()
        self.__get_and_advance_token(')')
        self.__get_and_advance_token(';')
        self.vm_writer.write_call(subroutine_name, n_args)
        self.__analysis_output.write('</doStatement>\n')


    def __compile_return_statement(self):
        self.__analysis_output.write('<returnStatement>\n')
        self.__get_and_advance_token('return')
        if self.tokenizer.get_current_token() != ';':
            self.__compile_expression()
        self.__get_and_advance_token(';')
        self.vm_writer.write_return()
        self.__analysis_output.write('</returnStatement>\n')


    """ Compile Expression """
    def __compile_expression(self):
        self.__analysis_output.write('<expression>\n')
        self.__compile_term()
        while self.tokenizer.get_current_token() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            op = self.__get_and_advance_token(['+', '-', '*', '/', '&', '|', '<', '>', '='])
            self.__compile_term()
            if op == '+':
                self.vm_writer.write_arithmetic('add')
            elif op == '-':
                self.vm_writer.write_arithmetic('sub')
            elif op == '*':
                self.vm_writer.write_call('Math.multiply', 2)
            elif op == '/':
                self.vm_writer.write_call('Math.divide', 2)
            elif op == '&':
                self.vm_writer.write_arithmetic('and')
            elif op == '|':
                self.vm_writer.write_arithmetic('or')
            elif op == '<':
                self.vm_writer.write_arithmetic('lt')
            elif op == '>':
                self.vm_writer.write_arithmetic('gt')
            elif op == '=':
                self.vm_writer.write_arithmetic('eq')
        self.__analysis_output.write('</expression>\n')


    def __compile_term(self):
        self.__analysis_output.write('<term>\n')
        if self.tokenizer.token_type() == 'INT_CONST':
            val = self.__get_and_advance_token(valid_token_type='INT_CONST')
            self.vm_writer.write_push('constant', val)
        elif self.tokenizer.token_type() == 'STRING_CONST':
            self.__get_and_advance_token(valid_token_type='STRING_CONST')
        elif self.tokenizer.get_current_token() in ['true', 'false', 'null', 'this']:
            self.__get_and_advance_token(['true', 'false', 'null', 'this'])
        elif self.tokenizer.get_current_token() == '(':
            self.__get_and_advance_token('(')
            self.__compile_expression()
            self.__get_and_advance_token(')')
        elif self.tokenizer.get_current_token() in ['-', '~']:
            self.__get_and_advance_token(['-', '~'])
            self.__compile_term()
        elif self.tokenizer.token_type() == 'IDENTIFIER':
            if self.tokenizer.get_next_token() == '[':
                self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="var/use")
                self.__get_and_advance_token('[')
                self.__compile_expression()
                self.__get_and_advance_token(']')
            elif self.tokenizer.get_next_token() == '.':
                self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="class/use")
                self.__get_and_advance_token('.')
                self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="subroutine/use")
                self.__get_and_advance_token('(')
                self.__compile_expression_list()
                self.__get_and_advance_token(')')
            elif self.tokenizer.get_next_token() == '(':
                self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="subroutine/use")
                self.__get_and_advance_token('(')
                self.__compile_expression_list()
                self.__get_and_advance_token(')')
            else:
                self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="var/use")
        self.__analysis_output.write('</term>\n')


    def __compile_expression_list(self):
        self.__analysis_output.write('<expressionList>\n')
        n_args = 0
        if self.tokenizer.get_current_token() != ')':
            self.__compile_expression()
            n_args += 1
            while self.tokenizer.get_current_token() == ',':
                self.__get_and_advance_token(',')
                self.__compile_expression()
                n_args += 1
        self.__analysis_output.write('</expressionList>\n')
        return n_args


    """ Utils """
    def __get_and_advance_token(self, valid_tokens=None, valid_token_type=None, metadata=""):
        if isinstance(valid_tokens, str):
            valid_tokens = [valid_tokens]
        token = self.tokenizer.get_current_token()
        token_type = self.tokenizer.token_type()
        if (valid_tokens and not token in valid_tokens) or (valid_token_type  and token_type != valid_token_type):
            raise Exception('Invalid syntax: ' + token + ' (expected ' + token_type + ')')

        token_type = token_type.lower().replace('int_const', 'integerConstant').replace('string_const', 'stringConstant')
        if token_type == 'keyword':
            token = self.tokenizer.key_word()
        elif token_type == 'symbol':
            token = self.tokenizer.symbol().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        elif token_type == 'identifier':
            token = self.tokenizer.identifier()
        elif token_type == 'integerConstant':
            token = str(self.tokenizer.int_val())
        elif token_type == 'stringConstant':
            token = self.tokenizer.string_val()
        else:
            raise Exception("Invalid token type: " + token_type)
        self.__analysis_output.write('<' + token_type + '>')
        self.__analysis_output.write(token)
        if metadata and CompilationEngine.WRITE_METADATA:
            self.__analysis_output.write('(' + metadata + ')')  # for chapter 11
        self.__analysis_output.write('</' + token_type + '>\n')
        self.tokenizer.advance()
        return token
