#!/usr/bin/env python

import re


class Parser(object):

    ARITHEMTIC_COMMANDS = ['add', 'sub', 'neg',
                           'eq', 'gt', 'lt',
                           'and', 'or', 'not']
    PUSH_COMMAND = 'push'
    POP_COMMAND = 'pop'

    def __init__(self, file_name):
        super(Parser, self).__init__()
        self.__lines = open(file_name).readlines()
        # remove comment and blank lines
        self.__lines = map(
            lambda l: re.sub(r'//.*|^\s*|\n', '', l), self.__lines)
        self.__lines = filter(lambda l: l, self.__lines)
        self.__current_line_idx = -1

    @property
    def current_line(self):
        if 0 <= self.__current_line_idx < len(self.__lines):
            return self.__lines[self.__current_line_idx]
        else:
            return None

    def has_more_commands(self):
        return self.__current_line_idx + 1 < len(self.__lines)

    def advance(self):
        self.__current_line_idx += 1

    def command_type(self):
        words = self.current_line.split()
        command = words[0]
        self.__arg1 = words[1] if len(words) > 1 else None
        self.__arg2 = words[2] if len(words) > 2 else None

        if command in Parser.ARITHEMTIC_COMMANDS:
            self.__arg1 = command
            return 'C_ARITHEMTIC'
        elif command == Parser.PUSH_COMMAND:
            return 'C_PUSH'
        elif command == Parser.POP_COMMAND:
            return 'C_POP'

        return 'C_LABEL'
        return 'C_GOTO'
        return 'C_IF'
        return 'C_FUNCTION'
        return 'C_RETURN'
        return 'C_CALL'

    def arg1(self):
        return self.__arg1

    def arg2(self):
        return self.__arg2

    def seek_head(self):
        self.__current_line_idx = -1
        return
