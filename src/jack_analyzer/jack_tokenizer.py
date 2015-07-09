#!/usr/bin/env python
import re


class JackTokenizer(object):
    """docstring for JackTokenizer"""
    def __init__(self, file_name):
        super(JackTokenizer, self).__init__()
        source = open(file_name).read()
        self.__tokens = re.split(r'//.*\n|/\*[\s\S]*?\*/|//.*|\s+|\n+', source)
        self.__tokens = list(filter(lambda t: t, self.__tokens))
        self.__current_line_idx = -1

    def has_more_tokens(self):
        return self.__current_line_idx + 1 < len(self.__tokens)

    def advance(self):
        self.__current_line_idx += 1

    def token_type(self):
        pass

    def key_word(self):
        pass

    def symbol(self):
        pass

    def identifier(self):
        pass

    def int_val(self):
        pass

    def string_val(self):
        pass

    def get_current_token(self):
        return self.__tokens[self.__current_line_idx]
