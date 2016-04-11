#!/usr/bin/env python


class VMWriter(object):

    def __init__(self, output):
        super(VMWriter, self).__init__()
        self.__output = output

    def write_push(self, segment, index):
        pass

    def write_pop(self, segment, index):
        pass

    def write_arithmetic(command):
        pass

    def write_label(self, label):
        pass

    def write_goto(self, label):
        pass

    def write_if(self, label):
        pass

    def write_call(self, name, n_args):
        pass

    def write_function(self, name, n_locals):
        self.__output.write('function ')
        self.__output.write(name + ' ')
        self.__output.write(str(n_locals))
        self.__output.write('\n')

    def write_return(self):
        pass
