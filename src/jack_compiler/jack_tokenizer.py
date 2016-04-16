#!/usr/bin/env python
import re


RE_COMMENT = r'//.*\n|/\*[\s\S]*?\*/|//.*|\s+|\n+'

RE_KEYWORD = r'class$|constructor$|function$|method$|field$|static$|' + \
r'var$|int$|char$|boolean$|void$|true$|false$|null$|this$|let$|do$|if$|else$|while$|return$'

RE_SYMBOL = r'{|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~'

RE_INT_CONST = r'3276[0-7]|327[0-5]\d|32[0-6]\d{2}|3[0-1]\d{3}|[0-2]{4}|\d{1,4}'

RE_STRING_CONST = r'\".*\"'

RE_IDENTIFIER = r'[a-zA-Z_]\w*'

RE_SPLIT = RE_COMMENT + \
    '|(' + RE_KEYWORD + ')' + \
    '|(' + RE_SYMBOL + ')' + \
    '|(' + RE_INT_CONST + ')' + \
    '|(' + RE_STRING_CONST + ')' + \
    '|(' + RE_IDENTIFIER + ')'

class JackTokenizer(object):

    def __init__(self, file_name):
        super(JackTokenizer, self).__init__()
        source = open(file_name).read()
        self.__tokens = re.split(RE_SPLIT, source)
        self.__tokens = list(filter(lambda t: t, self.__tokens))
        self.__current_line_idx = -1


    def has_more_tokens(self):
        return self.__current_line_idx + 1 < len(self.__tokens)


    def advance(self):
        self.__current_line_idx += 1


    def token_type(self):
        token = self.get_current_token()
        if re.match(RE_KEYWORD, token):
            return 'KEYWORD'
        elif re.match(RE_SYMBOL, token):
            return 'SYMBOL'
        elif re.match(RE_IDENTIFIER, token):
            return 'IDENTIFIER'
        elif re.match(RE_INT_CONST, token):
            return 'INT_CONST'
        elif re.match(RE_STRING_CONST, token):
            return 'STRING_CONST'
        else:
            raise Exception("unrecognizable token: " + token)


    def key_word(self):
        return self.get_current_token()


    def symbol(self):
        return self.get_current_token()


    def identifier(self):
        return self.get_current_token()


    def int_val(self):
        return int(self.get_current_token())


    def string_val(self):
        return self.get_current_token().replace("\"", "")


    def get_current_token(self):
        return self.__tokens[self.__current_line_idx]


    def get_next_token(self):
        return self.__tokens[self.__current_line_idx+1]
