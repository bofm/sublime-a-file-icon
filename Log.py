# -*- coding: utf-8 -*-

DEBUG = False


def message(*args):
    if DEBUG:
        text = ['zzFileIcons: ']
        for arg in args:
            text.append(str(arg))
        print(''.join(text))


def value(*args):
    if DEBUG:
        text = ['         >>> ']
        for arg in args:
            text.append(str(arg))
        print(''.join(text))


def separator():
    if DEBUG:
        print('\n***\n')
