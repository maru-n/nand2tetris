#!/usr/bin/env python


class CompilationEngine(object):

    def __init__(self, tokenizer, output):
        super(CompilationEngine, self).__init__()
        self.__target = output
        self.__tokenizer = tokenizer


    def compile(self):
        if not self.__tokenizer.has_more_tokens():
            raise Exception('Invalid EOF.')
        self.__tokenizer.advance()
        self.__compile_class()


    """ Program """
    def __compile_class(self):
        self.__target.write('<class>\n')
        self.__compile_terminal('class')
        self.__compile_class_name()
        self.__compile_terminal('{')
        while self.__is_class_var_dec():
            self.__compile_class_var_dec()
        while self.__is_subroutine_dec():
            self.__compile_subroutine_dec()
        self.__compile_terminal('}')
        self.__target.write('</class>\n')


    def __is_class_var_dec(self):
        return self.__is_terminal(['static', 'field'])

    def __compile_class_var_dec(self):
        self.__target.write('<classVarDec>\n')
        self.__compile_terminal(['static', 'field'])
        self.__compile_type()
        self.__compile_var_name()
        while self.__is_terminal(','):
            self.__compile_terminal(',')
            self.__compile_var_name()
        self.__compile_terminal(';')
        self.__target.write('</classVarDec>\n')


    def __is_type(self):
        if self.__is_terminal(['int', 'char', 'boolean']):
            return True
        elif self.__is_class_name():
            return True
        else:
            return False

    def __compile_type(self):
        if self.__is_terminal(['int', 'char', 'boolean']):
            self.__compile_terminal(['int', 'char', 'boolean'])
        else:
            self.__compile_class_name()


    def __is_subroutine_dec(self):
        return self.__is_terminal(['constructor', 'function', 'method'])

    def __compile_subroutine_dec(self):
        self.__target.write('<subroutineDec>\n')
        self.__compile_terminal(['constructor', 'function', 'method'])
        if self.__is_terminal('void'):
            self.__compile_terminal('void')
        else:
            self.__compile_type()
        self.__compile_subroutine_name()
        self.__compile_terminal('(')
        self.__compile_parameter_list()
        self.__compile_terminal(')')
        self.__compile_subroutine_dec_body()
        self.__target.write('</subroutineDec>\n')


    def __compile_parameter_list(self):
        self.__target.write('<parameterList>\n')
        if self.__is_type():
            self.__compile_type()
            self.__compile_var_name()
            while self.__is_terminal(','):
                self.__compile_terminal(',')
                self.__compile_type()
                self.__compile_var_name()
        self.__target.write('</parameterList>\n')


    def __compile_subroutine_dec_body(self):
        self.__target.write('<subroutineBody>\n')
        self.__compile_terminal('{')
        while self.__is_var_dec():
            self.__compile_var_dec()
        self.__compile_statements()
        self.__compile_terminal('}')
        self.__target.write('</subroutineBody>\n')


    def __is_var_dec(self):
        return self.__is_terminal('var')

    def __compile_var_dec(self):
        self.__target.write('<varDec>\n')
        self.__compile_terminal('var')
        self.__compile_type()
        self.__compile_var_name()
        while self.__is_terminal(','):
            self.__compile_terminal(',')
            self.__compile_var_name()
        self.__compile_terminal(';')
        self.__target.write('</varDec>\n')


    def __is_class_name(self):
        return self.__is_terminal(terminal_type='IDENTIFIER')

    def __compile_class_name(self):
        self.__compile_terminal(terminal_type='IDENTIFIER')


    def __is_subroutine_name(self):
        return self.__is_terminal(terminal_type='IDENTIFIER')

    def __compile_subroutine_name(self):
        self.__compile_terminal(terminal_type='IDENTIFIER')


    def __is_var_name(self):
        return self.__is_terminal(terminal_type='IDENTIFIER')

    def __compile_var_name(self):
        self.__compile_terminal(terminal_type='IDENTIFIER')


    """ Statement """
    def __compile_statements(self):
        self.__target.write('<statements>\n')
        while self.__is_statement():
            self.__compile_statement()
        self.__target.write('</statements>\n')


    def __is_statement(self):
        return self.__is_let_statement() or \
            self.__is_if_statement() or \
            self.__is_while_statement() or \
            self.__is_do_statement() or \
            self.__is_return_statement()

    def __compile_statement(self):
        if self.__is_let_statement():
            self.__compile_let_statement()
        elif self.__is_if_statement():
            self.__compile_if_statement()
        elif self.__is_while_statement():
            self.__compile_while_statement()
        elif self.__is_do_statement():
            self.__compile_do_statement()
        elif self.__is_return_statement():
            self.__compile_return_statement()


    def __is_let_statement(self):
        return self.__is_terminal('let')

    def __compile_let_statement(self):
        self.__target.write('<letStatement>\n')
        self.__compile_terminal('let')
        self.__compile_var_name()
        if self.__is_terminal('['):
            self.__compile_terminal('[')
            self.__compile_expression()
            self.__compile_terminal(']')
        self.__compile_terminal('=')
        self.__compile_expression()
        self.__compile_terminal(';')
        self.__target.write('</letStatement>\n')


    def __is_if_statement(self):
        return self.__is_terminal('if')

    def __compile_if_statement(self):
        self.__target.write('<ifStatement>\n')
        self.__compile_terminal('if')
        self.__compile_terminal('(')
        self.__compile_expression()
        self.__compile_terminal(')')
        self.__compile_terminal('{')
        self.__compile_statements()
        self.__compile_terminal('}')
        if self.__is_terminal('else'):
            self.__compile_terminal('else')
            self.__compile_terminal('{')
            self.__compile_statements()
            self.__compile_terminal('}')
        self.__target.write('</ifStatement>\n')

    def __is_while_statement(self):
        return self.__is_terminal('while')

    def __compile_while_statement(self):
        self.__target.write('<whileStatement>\n')
        self.__compile_terminal('while')
        self.__compile_terminal('(')
        self.__compile_expression()
        self.__compile_terminal(')')
        self.__compile_terminal('{')
        self.__compile_statements()
        self.__compile_terminal('}')
        self.__target.write('</whileStatement>\n')


    def __is_do_statement(self):
        return self.__is_terminal('do')

    def __compile_do_statement(self):
        self.__target.write('<doStatement>\n')
        self.__compile_terminal('do')
        self.__compile_subroutine_call()
        self.__compile_terminal(';')
        self.__target.write('</doStatement>\n')


    def __is_return_statement(self):
        return self.__is_terminal('return')

    def __compile_return_statement(self):
        self.__target.write('<returnStatement>\n')
        self.__compile_terminal('return')
        if self.__is_expression():
            self.__compile_expression()
        self.__compile_terminal(';')
        self.__target.write('</returnStatement>\n')


    """ Expression """
    TERMINAL_OP = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
    TERMINAL_UNARY_OP = ['-', '~']
    TERMINAL_KEYWORD_CONSTANT = ['true', 'false', 'null', 'this']

    def __is_expression(self):
        return self.__is_term()

    def __compile_expression(self):
        self.__target.write('<expression>\n')
        self.__compile_term()
        while self.__is_terminal(CompilationEngine.TERMINAL_OP):
            self.__compile_terminal(CompilationEngine.TERMINAL_OP)
            self.__compile_term()
        self.__target.write('</expression>\n')


    def __is_term(self):
        int_const = self.__is_terminal(terminal_type='INT_CONST')
        str_const = self.__is_terminal(terminal_type='STRING_CONST')
        kw_const = self.__is_terminal(CompilationEngine.TERMINAL_KEYWORD_CONSTANT)
        var_array = self.__is_var_name()
        sr_call = self.__is_subroutine_call()
        group = self.__is_terminal('(')
        anary_op = self.__is_terminal(CompilationEngine.TERMINAL_UNARY_OP)
        return (int_const or str_const or kw_const or var_array or sr_call or group or anary_op)

    def __compile_term(self):
        self.__target.write('<term>\n')
        if self.__is_terminal(terminal_type='INT_CONST'):
            self.__compile_terminal(terminal_type='INT_CONST')
        elif self.__is_terminal(terminal_type='STRING_CONST'):
            self.__compile_terminal(terminal_type='STRING_CONST')
        elif self.__is_terminal(CompilationEngine.TERMINAL_KEYWORD_CONSTANT):
            self.__compile_terminal(CompilationEngine.TERMINAL_KEYWORD_CONSTANT)
        elif self.__is_subroutine_call():
            self.__compile_subroutine_call()
        elif self.__is_var_name():
            self.__compile_var_name()
            if self.__is_terminal('['):
                self.__compile_terminal('[')
                self.__compile_expression()
                self.__compile_terminal(']')
        elif self.__is_terminal('('):
            self.__compile_terminal('(')
            self.__compile_expression()
            self.__compile_terminal(')')
        elif self.__is_terminal(CompilationEngine.TERMINAL_UNARY_OP):
            self.__compile_terminal(CompilationEngine.TERMINAL_UNARY_OP)
            self.__compile_term()
        self.__target.write('</term>\n')


    def __is_subroutine_call(self):
        func = self.__is_subroutine_name() and self.__tokenizer.get_next_token() is "("
        method = (self.__is_class_name() or self.__is_var_name()) and self.__tokenizer.get_next_token() is '.'
        return func or method

    def __compile_subroutine_call(self):
        while not self.__is_terminal('('):
            self.__compile_terminal()
        self.__compile_terminal('(')
        self.__compile_expression_list()
        self.__compile_terminal(')')


    def __compile_expression_list(self):
        self.__target.write('<expressionList>\n')
        if self.__is_expression():
            self.__compile_expression()
            while self.__is_terminal(','):
                self.__compile_terminal(',')
                self.__compile_expression()
        self.__target.write('</expressionList>\n')


    """ Lexical elements """
    def __is_terminal(self, terminals=None, terminal_type=None):
        if isinstance(terminals, str):
            terminals = [terminals]
        if terminals and not self.__tokenizer.get_current_token() in terminals:
            return False
        if terminal_type is not None and self.__tokenizer.token_type() is not terminal_type:
            return False
        return True

    def __compile_terminal(self, terminals=None, terminal_type=None):
        if not self.__is_terminal(terminals, terminal_type):
            raise Exception('Invalid syntax: '+self.__tokenizer.get_current_token())
        self.__output_current_token()
        self.__tokenizer.advance()


    def __output_current_token(self):
        token_type = self.__tokenizer.token_type()
        if token_type == 'KEYWORD':
            self.__target.write('<keyword>')
            self.__target.write(self.__tokenizer.key_word())
            self.__target.write('</keyword>')
        elif token_type == 'SYMBOL':
            self.__target.write('<symbol>')
            symbol = self.__tokenizer.symbol()
            if symbol == '<':
                symbol = '&lt;'
            elif symbol == '>':
                symbol = '&gt;'
            elif symbol == '&':
                symbol = '&amp;'
            self.__target.write(symbol)
            self.__target.write('</symbol>')
        elif token_type == 'IDENTIFIER':
            self.__target.write('<identifier>')
            self.__target.write(self.__tokenizer.identifier())
            self.__target.write('</identifier>')
        elif token_type == 'INT_CONST':
            self.__target.write('<integerConstant>')
            self.__target.write(str(self.__tokenizer.int_val()))
            self.__target.write('</integerConstant>')
        elif token_type == 'STRING_CONST':
            self.__target.write('<stringConstant>')
            self.__target.write(self.__tokenizer.string_val())
            self.__target.write('</stringConstant>')
        self.__target.write('\n')
