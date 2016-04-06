#!/usr/bin/env python

import sys
import glob
from os import path
from compilation_engine import CompilationEngine


def analyze(src_jack_file, output):
    print(src_jack_file)
    compilation_engine = CompilationEngine(src_jack_file, output)
    compilation_engine.compile()


if __name__ == '__main__':
    input_file = sys.argv[1]

    if path.isfile(input_file):
        src_jack_files = [input_file]
    else:
        src_jack_files = glob.glob(path.join(sys.argv[1], '*.jack'))

    for src_jack_file in src_jack_files:
        #output = sys.stdout
        output = open(path.splitext(src_jack_file)[0] + ".xml", 'w')
        analyze(src_jack_file, output)
