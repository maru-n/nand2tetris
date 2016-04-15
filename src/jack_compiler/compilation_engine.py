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
        self.__unique_label_index = 0

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
        self.__analysis_write('<class>\n')
        self.__advance_tokens('class')
        self.__class_name = self.__get_and_advance_token(valid_token_type='IDENTIFIER')
        self.__advance_tokens('{')
        while self.tokenizer.get_current_token() in ['static', 'field']:
            self.__compile_class_var_dec()
        while self.tokenizer.get_current_token() in ['constructor', 'function', 'method']:
            self.__compile_subroutine_dec()
        self.__advance_tokens('}')
        self.__analysis_write('</class>\n')


    def __compile_class_var_dec(self):
        self.__analysis_write('<classVarDec>\n')
        var_kind = self.__get_and_advance_token(['static', 'field'])
        var_type = self.__get_token_as_var_type()
        var_name = self.__get_and_advance_token(valid_token_type='IDENTIFIER')
        self.symbol_table.define(var_name, var_type, var_kind)
        while self.tokenizer.get_current_token() == ',':
            self.__advance_tokens(',')
            var_name = self.__get_and_advance_token(valid_token_type='IDENTIFIER')
            self.symbol_table.define(var_name, var_type, var_kind)
        self.__advance_tokens(';')
        self.__analysis_write('</classVarDec>\n')


    def __compile_subroutine_dec(self):
        self.__analysis_write('<subroutineDec>\n')
        self.symbol_table.start_subroutine()
        func_type = self.__get_and_advance_token(['constructor', 'function', 'method'])
        if self.tokenizer.get_current_token() == 'void':
            self.__get_and_advance_token('void')
        else:
            self.__get_token_as_var_type()
        self.__current_func_name = self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="subroutine/defined")
        self.__get_and_advance_token('(')
        param_num = self.__compile_parameter_list()
        self.__get_and_advance_token(')')
        self.__compile_subroutine_body()
        self.__analysis_write('</subroutineDec>\n')


    def __compile_parameter_list(self):
        self.__analysis_write('<parameterList>\n')
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
        self.__analysis_write('</parameterList>\n')
        return param_cnt


    def __compile_subroutine_body(self):
        self.__analysis_write('<subroutineBody>\n')
        self.__advance_tokens('{')
        n_locals = 0
        while self.tokenizer.get_current_token() == 'var':
            n_locals += self.__compile_var_dec()
        self.vm_writer.write_function(self.__class_name+'.'+self.__current_func_name, n_locals)
        self.__compile_statements()
        self.__advance_tokens('}')
        self.__analysis_write('</subroutineBody>\n')


    def __compile_var_dec(self):
        self.__analysis_write('<varDec>\n')
        self.__advance_tokens('var')
        var_type = self.__get_token_as_var_type()
        var_name = self.__get_and_advance_token(valid_token_type="IDENTIFIER", metadata="var/defined")
        self.symbol_table.define(var_name, var_type, 'VAR')
        cnt = 1
        while self.tokenizer.get_current_token() == ',':
            self.__advance_tokens(',')
            var_name = self.__get_and_advance_token(valid_token_type="IDENTIFIER", metadata="var/defined")
            self.symbol_table.define(var_name, var_type, 'VAR')
            cnt += 1
        self.__advance_tokens(';')
        self.__analysis_write('</varDec>\n')
        return cnt


    def __get_token_as_var_type(self):
        try:
            var_type = self.__get_and_advance_token(['int', 'char', 'boolean'])
        except:
            var_type = self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="class/use")
        return var_type


    def __compile_statements(self):
        self.__analysis_write('<statements>\n')
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
        self.__analysis_write('</statements>\n')


    def __compile_let_statement(self):
        self.__analysis_write('<letStatement>\n')
        self.__advance_tokens('let')
        var_name = self.__get_and_advance_token(valid_token_type='IDENTIFIER')
        if self.tokenizer.get_current_token() == '[':
            self.__advance_tokens('[')
            self.__compile_expression()
            self.__advance_tokens(']')
        self.__advance_tokens('=')
        self.__compile_expression()
        self.__advance_tokens(';')
        segment = self.__convert_symbol_kind_to_segment(self.symbol_table.kind_of(var_name))
        index = self.symbol_table.index_of(var_name)
        self.vm_writer.write_pop(segment, index)
        self.__analysis_write('</letStatement>\n')


    def __compile_if_statement(self):
        self.__analysis_write('<ifStatement>\n')
        label1 = self.__get_unique_vm_label()
        label2 = self.__get_unique_vm_label()
        self.__advance_tokens(['if', '('])
        self.__compile_expression()
        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_if(label1)
        self.__advance_tokens([')', '{'])
        self.__compile_statements()
        self.vm_writer.write_goto(label2)
        self.__advance_tokens('}')
        self.vm_writer.write_label(label1)
        if self.tokenizer.get_current_token() == 'else':
            self.__advance_tokens(['else', '{'])
            self.__compile_statements()
            self.__advance_tokens('}')
        self.vm_writer.write_label(label2)
        self.__analysis_write('</ifStatement>\n')


    def __compile_while_statement(self):
        label1 = self.__get_unique_vm_label()
        label2 = self.__get_unique_vm_label()
        self.__analysis_write('<whileStatement>\n')
        self.__advance_tokens(['while', '('])
        self.vm_writer.write_label(label1)
        self.__compile_expression()
        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_if(label2)
        self.__advance_tokens([')', '{'])
        self.__compile_statements()
        self.vm_writer.write_goto(label1)
        self.__advance_tokens('}')
        self.vm_writer.write_label(label2)
        self.__analysis_write('</whileStatement>\n')



    def __compile_do_statement(self):
        self.__analysis_write('<doStatement>\n')
        self.__get_and_advance_token('do')
        self.__compile_call_subroutine()
        self.__advance_tokens(';')
        self.__analysis_write('</doStatement>\n')


    def __compile_return_statement(self):
        self.__analysis_write('<returnStatement>\n')
        self.__advance_tokens('return')
        if self.tokenizer.get_current_token() != ';':
            self.__compile_expression()
        self.__advance_tokens(';')
        self.vm_writer.write_return()
        self.__analysis_write('</returnStatement>\n')


    def __compile_call_subroutine(self):
        subroutine_name = ""
        if self.tokenizer.get_next_token() == ".":
            subroutine_name += self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="class/use")
            subroutine_name += self.__get_and_advance_token('.')
        subroutine_name += self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="subroutine/use")
        self.__advance_tokens('(')
        n_args = self.__compile_expression_list()
        self.__advance_tokens(')')
        self.vm_writer.write_call(subroutine_name, n_args)


    def __compile_expression(self):
        self.__analysis_write('<expression>\n')
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
        self.__analysis_write('</expression>\n')


    def __compile_term(self):
        self.__analysis_write('<term>\n')
        if self.tokenizer.token_type() == 'INT_CONST':
            val = self.__get_and_advance_token(valid_token_type='INT_CONST')
            self.vm_writer.write_push('constant', val)
        elif self.tokenizer.token_type() == 'STRING_CONST':
            self.__get_and_advance_token(valid_token_type='STRING_CONST')
        elif self.tokenizer.get_current_token() == 'true':
            self.__advance_tokens('true')
            self.vm_writer.write_push('constant', 1)
            self.vm_writer.write_arithmetic('neg')
        elif self.tokenizer.get_current_token() == 'false':
            self.__advance_tokens('false')
            self.vm_writer.write_push('constant', 0)
        elif self.tokenizer.get_current_token() == 'null':
            self.__advance_tokens('null')
            self.vm_writer.write_push('constant', 0)
        elif self.tokenizer.get_current_token() == 'this':
            self.__advance_tokens('this')
        elif self.tokenizer.get_current_token() == '(':
            self.__advance_tokens('(')
            self.__compile_expression()
            self.__advance_tokens(')')
        elif self.tokenizer.get_current_token() in ['-', '~']:
            op = self.__get_and_advance_token(['-', '~'])
            self.__compile_term()
            if op == '-':
                self.vm_writer.write_arithmetic('neg')
            elif op == '~':
                self.vm_writer.write_arithmetic('not')
        elif self.tokenizer.token_type() == 'IDENTIFIER':
            if self.tokenizer.get_next_token() == '[':
                self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="var/use")
                self.__get_and_advance_token('[')
                self.__compile_expression()
                self.__get_and_advance_token(']')
            elif self.tokenizer.get_next_token() in ['.', '(']:
                self.__compile_call_subroutine()
            else:
                var_name = self.__get_and_advance_token(valid_token_type='IDENTIFIER', metadata="var/use")
                index = self.symbol_table.index_of(var_name)
                segment = self.__convert_symbol_kind_to_segment(self.symbol_table.kind_of(var_name))
                self.vm_writer.write_push(segment, index)
        self.__analysis_write('</term>\n')


    def __compile_expression_list(self):
        self.__analysis_write('<expressionList>\n')
        n_args = 0
        if self.tokenizer.get_current_token() != ')':
            self.__compile_expression()
            n_args += 1
            while self.tokenizer.get_current_token() == ',':
                self.__advance_tokens(',')
                self.__compile_expression()
                n_args += 1
        self.__analysis_write('</expressionList>\n')
        return n_args


    def __get_unique_vm_label(self):
        label = self.__class_name.upper() + '_CONTROLL_' + str(self.__unique_label_index)
        self.__unique_label_index += 1
        return label


    def __convert_symbol_kind_to_segment(self, symbol_kinde):
        if symbol_kinde == 'STATIC':
            segment = 'static'
        elif symbol_kinde == 'FIELD':
            segment = 'argument'
        elif symbol_kinde == 'ARG':
            segment = 'argument'
        elif symbol_kinde == 'VAR':
            segment = 'local'
        else:
            raise Exception("Not defined variable: " + var_name)
        return segment


    def __advance_tokens(self, tokens):
        if isinstance(tokens, str):
            tokens = [tokens]
        for token in tokens:
            self.__get_and_advance_token(token)


    def __get_and_advance_token(self, valid_tokens=None, valid_token_type=None, metadata=""):
        token_type = self.tokenizer.token_type()
        if valid_token_type  and token_type != valid_token_type:
            raise Exception('Invalid token type: ' + token_type + ' (expected ' + token_type + ')')

        if token_type == 'KEYWORD':
            token_type_xml = token_type.lower()
            token = self.tokenizer.key_word()
        elif token_type == 'SYMBOL':
            token_type_xml = token_type.lower()
            token = self.tokenizer.symbol()
        elif token_type == 'IDENTIFIER':
            token_type_xml = token_type.lower()
            token = self.tokenizer.identifier()
        elif token_type == 'INT_CONST':
            token_type_xml = 'integerConstant'
            token = str(self.tokenizer.int_val())
        elif token_type == 'STRING_CONST':
            token_type_xml = 'stringConstant'
            token = self.tokenizer.string_val()
        else:
            raise Exception("Invalid token type: " + token_type)

        if isinstance(valid_tokens, str):
            valid_tokens = [valid_tokens]
        if valid_tokens and not token in valid_tokens:
            raise Exception('Invalid token: ' + token + ' (expected ' + token + ')')

        token_xml = token.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        token_type_xml = token_type.lower().replace('int_const', 'integerConstant').replace('string_const', 'stringConstant')
        self.__analysis_write('<' + token_type_xml + '>')
        self.__analysis_write(token_xml)
        if metadata and CompilationEngine.WRITE_METADATA:
            self.__analysis_write('(' + metadata + ')')  # for chapter 11
        self.__analysis_write('</' + token_type_xml + '>\n')
        self.tokenizer.advance()
        return token


    def __analysis_write(self, str):
        try:
            self.__analysis_output.write(str)
        except AttributeError:
            pass
