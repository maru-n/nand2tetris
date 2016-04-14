#!/usr/bin/env python


class VMWriter(object):

    def __init__(self, output):
        super(VMWriter, self).__init__()
        self.__output = output


    def write_push(self, segment, index):
        self.__output.write('push ')
        self.__output.write(segment + ' ')
        self.__output.write(str(index))
        self.__output.write('\n')


    def write_pop(self, segment, index):
        self.__output.write('pop ')
        self.__output.write(segment + ' ')
        self.__output.write(str(index))
        self.__output.write('\n')


    def write_arithmetic(self, command):
        if command.lower() in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            self.__output.write(command.lower())
            self.__output.write('\n')
        else:
            raise Exception('Invalid VM command: ' + command)


    def write_label(self, label):
        self.__output.write('label ')
        self.__output.write(label)
        self.__output.write('\n')


    def write_goto(self, label):
        self.__output.write('goto ')
        self.__output.write(label)
        self.__output.write('\n')


    def write_if(self, label):
        self.__output.write('if-goto ')
        self.__output.write(label)
        self.__output.write('\n')


    def write_call(self, name, n_args):
        self.__output.write('call ')
        self.__output.write(name + ' ')
        self.__output.write(str(n_args))
        self.__output.write('\n')


    def write_function(self, name, n_locals):
        self.__output.write('function ')
        self.__output.write(name + ' ')
        self.__output.write(str(n_locals))
        self.__output.write('\n')


    def write_return(self):
        self.__output.write('return\n')


    def __convert_segment_string(self, segment_str):
        segment_str = segment_str.upper()
        segment_str = segment_str.replace('ARG', 'argument')
        segment_str = segment_str.replace('ARG', 'argument')
