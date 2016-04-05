#!/usr/bin/env python
from jack_tokenizer import JackTokenizer

class CompilationEngine(object):

    """docstring for CompilationEngine"""

    def __init__(self, src_jack_file, output):
        super(CompilationEngine, self).__init__()
        self.__target = output
        self.__tokenizer = JackTokenizer(src_jack_file)

    def compile(self):
        self.__target.write('<tokens>\n')
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
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
        self.__target.write('</tokens>\n')

    def __compile_class(self):
        pass

    def __compile_class_var_dec(self):
        pass

    def __compile_subroutine(self):
        pass

    def __compile_parameter_list(self):
        pass

    def __compile_var_dec(self):
        pass

    def __compile_statements(self):
        pass

    def __compile_do(self):
        pass

    def __compile_let(self):
        pass

    def __compile_while(self):
        pass

    def __compile_return(self):
        pass

    def __compile_if(self):
        pass

    def __compile_expression(self):
        pass

    def __compile_term(self):
        pass

    def compile_expression_list(self):
        pass
