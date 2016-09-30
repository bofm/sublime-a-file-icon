# -*- coding: utf-8 -*-

import sublime

DEBUG = False
WARN = 'Please restart Sulbime Text for the applied icons to take effect ...'


def log(*args):
    text = []

    for arg in args:
        text.append(str(arg))
    print(''.join(text))


def message(*args):
    if DEBUG:
        log('File Icons: ', *args)


def value(*args):
    if DEBUG:
        log('        >>> ', *args)


def done():
    if DEBUG:
        log('File Icons: ', 'Finished')
        log('***\n')


def separator():
    if DEBUG:
        log('\n***')


def warning():
    sublime.message_dialog(WARN)
