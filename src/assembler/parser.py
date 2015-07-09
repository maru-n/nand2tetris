#!/usr/bin/env python

import re


class Parser(object):

    """Hack Assembler Parser"""
    A_COMMAND_RE = r'@(?P<symbol>[\w\.$:]+)$'
    L_COMMAND_RE = r'\((?P<symbol>[\w\.$:]+)\)$'
    C_COMMAND_RE = r'((?P<dest>A?M?D?)=)?'\
                   '(?P<comp>[01\-\+\|\&\!ADM]{1,3})'\
                   '(;(?P<jump>J\w{2}))?'

    def __init__(self, file_name):
        super(Parser, self).__init__()
        self.__lines = open(file_name).readlines()
        self.__lines = map(lambda l: re.sub(r'//.*', '', l), self.__lines)
        self.__lines = map(lambda l: re.sub(r'\s|\n', '', l), self.__lines)
        self.__lines = list(filter(lambda l: l, self.__lines))
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
        match = re.match(Parser.A_COMMAND_RE, self.current_line)
        if match:
            self.__symbol = match.group('symbol')
            return 'A_COMMAND'
        match = re.match(Parser.L_COMMAND_RE, self.current_line)
        if match:
            self.__symbol = match.group('symbol')
            return 'L_COMMAND'
        match = re.match(Parser.C_COMMAND_RE, self.current_line)
        if match:
            self.__dest = match.group('dest')
            self.__comp = match.group('comp')
            self.__jump = match.group('jump')
            return 'C_COMMAND'

    def symbol(self):
        return self.__symbol

    def dest(self):
        return self.__dest

    def comp(self):
        return self.__comp

    def jump(self):
        return self.__jump

    def seek_head(self):
        self.__current_line_idx = -1
        return
