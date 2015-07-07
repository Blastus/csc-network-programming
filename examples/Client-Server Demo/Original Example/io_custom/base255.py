'''Module for string conversion.

This module provides two functions that allow
strings to be encoded and decoded in base 255.'''

__version__ = '1.0'

import sys as _sys

################################################################################

def encode(string, divide=1024):
    'Encode a string to base 255.'
    def encode(s):
        i = 0
        for c in s:
            i *= 257
            i += ord(c) + 1
        s = ''
        while i:
            s = chr(i % 254 + 2) + s
            i /= 254
        return s
    return '\1'.join(encode(string[index:index+divide]) for index in range(0, len(string), divide))

def decode(string):
    'Decode a string from base 255.'
    def decode(s):
        i = 0
        for c in s:
            i *= 254
            i += ord(c) - 2
        s = ''
        while i:
            s = chr(i % 257 - 1) + s
            i /= 257
        return s
    return ''.join(decode(string) for string in string.split('\1'))

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
