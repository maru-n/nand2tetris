#!/usr/bin/env python

import sys
import glob
from os import path
from jack_tokenizer import JackTokenizer


def analyze(src_jack_file):
    tokenizer = JackTokenizer(src_jack_file)
    while tokenizer.has_more_tokens():
        tokenizer.advance()
        print(tokenizer.get_current_token())


if __name__ == '__main__':
    input_file = sys.argv[1]

    if path.isfile(input_file):
        src_jack_files = [input_file]
    else:
        src_jack_files = glob.glob(path.join(sys.argv[1], '*.jack'))

    for src_jack_file in src_jack_files:
        analyze(src_jack_file)
