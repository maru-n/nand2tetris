#!/usr/bin/env python

from symbol_table import SymbolTable
from vm_writer import VMWriter
import os

class CompilationEngine(object):

    def __init__(self, tokenizer, symbol_table=None, vm_writer=None):
        super(CompilationEngine, self).__init__()
        self._analysis = False
        self._tokenizer = tokenizer
        self._symbol_table = symbol_table
        self._vm_writer = vm_writer


    def compile(self):
        if not self._tokenizer.has_more_tokens():
            raise Exception('Invalid EOF.')
        self._tokenizer.advance()
        self._compile_class()
        self._analysis = False

    def analysis(self, output):
        self._analysis = True
        self._analysis_output = output
        self.compile()

    """ Program """
    def _compile_class(self):
        self._analysis_write('<class>\n')
        self._get_and_advance_token('class')
        self._class_name = self._get_and_advance_token(valid_token_type='IDENTIFIER', metadata="class/defined")
        self._get_and_advance_token('{')
        while self._get_current_token() in ['static', 'field']:
            self._compile_class_var_dec()
        while self._get_current_token() in ['constructor', 'function', 'method']:
            self._compile_subroutine_dec()
        self._get_and_advance_token('}')
        self._analysis_write('</class>\n')


    def _compile_class_var_dec(self):
        self._analysis_write('<classVarDec>\n')
        var_kind = self._get_and_advance_token(['static', 'field'])
        var_type = self._get_token_as_var_type()
        var_name = self._get_and_advance_token(valid_token_type='IDENTIFIER', metadata=var_kind+"/defined")
        self._define_symbol(var_name, var_type, var_kind)
        while self._get_current_token() == ',':
            self._get_and_advance_token(',')
            var_name = self._get_and_advance_token(valid_token_type='IDENTIFIER', metadata=var_kind+"/defined")
            self._define_symbol(var_name, var_type, var_kind)
        self._get_and_advance_token(';')
        self._analysis_write('</classVarDec>\n')

    def _define_symbol(self, var_name, var_type, var_kind):
        if self._symbol_table:
            self._symbol_table.define(var_name, var_type, var_kind)

    def _compile_subroutine_dec(self):
        self._analysis_write('<subroutineDec>\n')
        func_type = self._get_and_advance_token(['constructor', 'function', 'method'])
        if self._get_current_token() == 'void':
            self._get_and_advance_token('void')
        else:
            self._compile_type()
        func_name = self._get_and_advance_token(valid_token_type='IDENTIFIER', metadata="subroutine/defined")
        self._get_and_advance_token('(')
        param_num = self._compile_parameter_list()
        self._get_and_advance_token(')')
        if not self._analysis:
            self._vm_writer.write_function(self._class_name+'.'+func_name, param_num)
        self._compile_subroutine_body()
        self._analysis_write('</subroutineDec>\n')


    def _compile_parameter_list(self):
        self._analysis_write('<parameterList>\n')
        param_cnt = 0
        if self._current_token_is_type():
            var_type = self._get_token_as_var_type()
            var_name = self._get_and_advance_token(valid_token_type='IDENTIFIER', metadata="argument/defined")
            self._define_symbol(var_name, var_type, 'ARG')
            param_cnt = 0
            while self._get_current_token() == ',':
                self._get_and_advance_token(',')
                var_type = self._get_token_as_var_type()
                var_name = self._get_and_advance_token(valid_token_type='IDENTIFIER', metadata="argument/defined")
                self._define_symbol(var_name, var_type, 'ARG')
                param_cnt += 1
        self._analysis_write('</parameterList>\n')
        return param_cnt

    def _get_token_as_var_type(self):
        try:
            var_type = self._get_and_advance_token(['int', 'char', 'boolean'])
        except:
            var_type = self._get_and_advance_token(valid_token_type='IDENTIFIER', metadata="class/use")
        return var_type


    def _current_token_is_type(self):
        return self._get_current_token() in ['int', 'char', 'boolean'] or self._get_current_token_type() == 'IDENTIFIER'

    def _compile_subroutine_body(self):
        if self._analysis:
            self._analysis_write('<subroutineBody>\n')
        self._get_and_advance_token('{')
        while self._get_current_token() == 'var':
            self._compile_var_dec()
        self._compile_statements()
        self._get_and_advance_token('}')
        if self._analysis:
            self._analysis_write('</subroutineBody>\n')


    def _compile_var_dec(self):
        self._analysis_write('<varDec>\n')
        self._get_and_advance_token('var')
        self._compile_type()
        var_name = self._get_and_advance_token(valid_token_type="IDENTIFIER", metadata="var/defined")
        #self._define_symbol(var_name, )
        while self._is_terminal(','):
            self._compile_terminal(',')
            var_name = self._get_and_advance_token(valid_token_type="IDENTIFIER", metadata="var/defined")
            #self._define_symbol(var_name, )
        self._compile_terminal(';')
        self._analysis_write('</varDec>\n')


    def _compile_type(self):
        if self._get_current_token() in ['int', 'char', 'boolean']:
            self._get_and_advance_token(['int', 'char', 'boolean'])
        else:
            self._get_and_advance_token(valid_token_type='IDENTIFIER', metadata="class/use")


    def _is_var_name(self):
        return self._is_terminal(terminal_type='IDENTIFIER')

    def _compile_var_name(self):
        self._compile_terminal(terminal_type='IDENTIFIER')


    """ Statement """
    def _compile_statements(self):
        self._analysis_write('<statements>\n')
        while self._get_current_token() in ['let', 'if', 'while', 'do', 'return']:
            if self._get_current_token() == 'let':
                self._compile_let_statement()
            elif self._get_current_token() == 'if':
                self._compile_if_statement()
            elif self._get_current_token() == 'while':
                self._compile_while_statement()
            elif self._get_current_token() == 'do':
                self._compile_do_statement()
            elif self._get_current_token() == 'return':
                self._compile_return_statement()
        self._analysis_write('</statements>\n')



    def _compile_let_statement(self):
        self._analysis_write('<letStatement>\n')
        self._compile_terminal('let')
        self._compile_var_name()
        if self._is_terminal('['):
            self._compile_terminal('[')
            self._compile_expression()
            self._compile_terminal(']')
        self._compile_terminal('=')
        self._compile_expression()
        self._compile_terminal(';')
        self._analysis_write('</letStatement>\n')


    def _compile_if_statement(self):
        self._analysis_write('<ifStatement>\n')
        self._compile_terminal('if')
        self._compile_terminal('(')
        self._compile_expression()
        self._compile_terminal(')')
        self._compile_terminal('{')
        self._compile_statements()
        self._compile_terminal('}')
        if self._is_terminal('else'):
            self._compile_terminal('else')
            self._compile_terminal('{')
            self._compile_statements()
            self._compile_terminal('}')
        self._analysis_write('</ifStatement>\n')


    def _compile_while_statement(self):
        self._analysis_write('<whileStatement>\n')
        self._compile_terminal('while')
        self._compile_terminal('(')
        self._compile_expression()
        self._compile_terminal(')')
        self._compile_terminal('{')
        self._compile_statements()
        self._compile_terminal('}')
        self._analysis_write('</whileStatement>\n')


    def _compile_do_statement(self):
        self._analysis_write('<doStatement>\n')
        self._compile_terminal('do')
        self._compile_subroutine_call()
        self._compile_terminal(';')
        self._analysis_write('</doStatement>\n')


    def _compile_return_statement(self):
        self._analysis_write('<returnStatement>\n')
        self._compile_terminal('return')
        if self._is_expression():
            self._compile_expression()
        self._compile_terminal(';')
        self._analysis_write('</returnStatement>\n')


    """ Expression """
    TERMINAL_OP = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
    TERMINAL_UNARY_OP = ['-', '~']
    TERMINAL_KEYWORD_CONSTANT = ['true', 'false', 'null', 'this']

    def _is_expression(self):
        return self._is_term()

    def _compile_expression(self):
        self._analysis_write('<expression>\n')
        self._compile_term()
        while self._is_terminal(CompilationEngine.TERMINAL_OP):
            self._compile_terminal(CompilationEngine.TERMINAL_OP)
            self._compile_term()
        self._analysis_write('</expression>\n')


    def _is_term(self):
        int_const = self._is_terminal(terminal_type='INT_CONST')
        str_const = self._is_terminal(terminal_type='STRING_CONST')
        kw_const = self._is_terminal(CompilationEngine.TERMINAL_KEYWORD_CONSTANT)
        var_array = self._is_var_name()
        sr_call = self._is_subroutine_call()
        group = self._is_terminal('(')
        anary_op = self._is_terminal(CompilationEngine.TERMINAL_UNARY_OP)
        return (int_const or str_const or kw_const or var_array or sr_call or group or anary_op)

    def _compile_term(self):
        self._analysis_write('<term>\n')
        if self._is_terminal(terminal_type='INT_CONST'):
            self._compile_terminal(terminal_type='INT_CONST')
        elif self._is_terminal(terminal_type='STRING_CONST'):
            self._compile_terminal(terminal_type='STRING_CONST')
        elif self._is_terminal(CompilationEngine.TERMINAL_KEYWORD_CONSTANT):
            self._compile_terminal(CompilationEngine.TERMINAL_KEYWORD_CONSTANT)
        elif self._is_subroutine_call():
            self._compile_subroutine_call()
        elif self._is_var_name():
            self._compile_var_name()
            if self._is_terminal('['):
                self._compile_terminal('[')
                self._compile_expression()
                self._compile_terminal(']')
        elif self._is_terminal('('):
            self._compile_terminal('(')
            self._compile_expression()
            self._compile_terminal(')')
        elif self._is_terminal(CompilationEngine.TERMINAL_UNARY_OP):
            self._compile_terminal(CompilationEngine.TERMINAL_UNARY_OP)
            self._compile_term()
        self._analysis_write('</term>\n')


    def _is_subroutine_call(self):
        is_func = self._is_terminal(terminal_type='IDENTIFIER') and self._tokenizer.get_next_token() == "("
        is_method = self._is_terminal(terminal_type='IDENTIFIER') and self._tokenizer.get_next_token() == '.'
        return (is_func or is_method)

    def _compile_subroutine_call(self):
        if self._tokenizer.get_next_token() == ".":
            self._get_and_advance_token(valid_token_type='IDENTIFIER', metadata="class/use")
            self._compile_terminal('.')
        self._get_and_advance_token(valid_token_type='IDENTIFIER', metadata="subroutine/use")
        self._compile_terminal('(')
        self._compile_expression_list()
        self._compile_terminal(')')


    def _compile_expression_list(self):
        self._analysis_write('<expressionList>\n')
        if self._is_expression():
            self._compile_expression()
            while self._is_terminal(','):
                self._compile_terminal(',')
                self._compile_expression()
        self._analysis_write('</expressionList>\n')


    """ Lexical elements """
    def _is_terminal(self, terminals=None, terminal_type=None):
        if isinstance(terminals, str):
            terminals = [terminals]
        if terminals and not self._get_current_token() in terminals:
            return False
        if terminal_type is not None and self._tokenizer.token_type() != terminal_type:
            return False
        return True

    def _compile_terminal(self, terminals=None, terminal_type=None):
        self._get_and_advance_token(terminals, terminal_type)


    def _get_current_token(self):
        return self._tokenizer.get_current_token()

    def _get_current_token_type(self):
        return self._tokenizer.token_type()

    def _get_and_advance_token(self, valid_tokens=None, valid_token_type=None, metadata=""):
        if isinstance(valid_tokens, str):
            valid_tokens = [valid_tokens]
        token = self._tokenizer.get_current_token()
        token_type = self._tokenizer.token_type()
        if (valid_tokens and not token in valid_tokens) or (valid_token_type  and token_type != valid_token_type):
            raise Exception('Invalid syntax: ' + token + ' (expected ' + token_type + ')')
        self._output_current_token(metadata=metadata)
        self._tokenizer.advance()
        return token


    def _output_current_token(self, metadata=""):
        token_type = self._tokenizer.token_type().lower()
        if token_type == 'keyword':
            token = self._tokenizer.key_word()
        elif token_type == 'symbol':
            token = self._tokenizer.symbol()
            token = token.replace('&', '&amp;')
            token = token.replace('<', '&lt;')
            token = token.replace('>', '&gt;')
        elif token_type == 'identifier':
            token = self._tokenizer.identifier()
        elif token_type == 'int_const':
            token_type = 'integerConstant'
            token = str(self._tokenizer.int_val())
        elif token_type == 'string_const':
            token_type = 'stringConstant'
            token = self._tokenizer.string_val()
        else:
            raise Exception("Invalid token type: " + token_type)
        self._analysis_write('<' + token_type + '>')
        self._analysis_write(token)
        if metadata:
            pass
            #self._analysis_write('(' + metadata + ')')  # for chapter 11
        self._analysis_write('</' + token_type + '>\n')

    def _analysis_write(self, str):
        if self._analysis:
            self._analysis_output.write(str)
