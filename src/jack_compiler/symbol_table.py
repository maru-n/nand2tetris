#!/usr/bin/env python


class SymbolTableRecord(object):
    def __init__(self, name, type, kind, index):
        self.name = name
        self.type = type
        self.kind = kind
        self.index = index


class SymbolTable(object):

    def __init__(self):
        super(SymbolTable, self).__init__()
        self.__class_table = {}
        self.__subroutine_table = {}
        self.__var_count = {'STATIC':0, 'FIELD':0, 'ARG':0, 'VAR':0}


    def start_subroutine(self):
        self.__subroutine_table = {}
        self.__var_count['ARG'] = 0
        self.__var_count['VAR'] = 0


    def define(self, name, type, kind):
        kind = kind.upper()
        if kind in ['STATIC', 'FIELD']:
            self.__class_table[name] = SymbolTableRecord(name, type, kind, self.var_count(kind))
        elif kind in ['ARG', 'VAR']:
            self.__subroutine_table[name] = SymbolTableRecord(name, type, kind, self.var_count(kind))
        else:
            raise Exception('Invalid kind of identifier. identifier:' + name + ' kind:' + kind)
        self.__increment_var_count(kind)


    def var_count(self, kind):
        return self.__var_count[kind]


    def __increment_var_count(self, kind):
        self.__var_count[kind] += 1


    def kind_of(self, name):
        if name in self.__class_table:
            return self.__class_table[name].kind
        elif name in self.__subroutine_table:
            return self.__subroutine_table[name].kind
        else:
            return None


    def type_of(self, name):
        if name in self.__class_table:
            return self.__class_table[name].type
        elif name in self.__subroutine_table:
            return self.__subroutine_table[name].type
        else:
            return None


    def index_of(self, name):
        if name in self.__class_table:
            return self.__class_table[name].index
        elif name in self.__subroutine_table:
            return self.__subroutine_table[name].index
        else:
            return None
