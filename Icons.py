# -*- coding: utf-8 -*-

import sublime
import os
import re
import zzFileIcons.Log as log

from zzFileIcons.Themes import SUPPORTED
from zzFileIcons.Template import TEMPLATE

PACKAGE_SETTINGS = 'File Icons.sublime-settings'
SUBLIME_SETTINGS = 'Preferences.sublime-settings'

CURRENT_UI_THEME = ''
CURRENT_SETTINGS = {
    'color': '',
    'color_on_hover': '',
    'color_on_select': '',
    'force_override': '',
    'opacity': '',
    'opacity_on_hover': '',
    'opacity_on_select': '',
    'size': ''
}

DEST = os.path.join('zzFileIcons', 'dist', 'zpatches')
SETTINGS_CHANGED = False


def get_sublime_settings():
    return sublime.load_settings(SUBLIME_SETTINGS)


def get_package_settings():
    return sublime.load_settings(PACKAGE_SETTINGS)


def get_dest_path():
    return os.path.join(sublime.packages_path(), DEST)


def get_installed_themes():
    log.message('Getting installed themes')

    installed_themes = {}

    for r in sublime.find_resources('*.sublime-theme'):
        installed_themes.setdefault(os.path.basename(os.path.dirname(r)),
                                    []).append(os.path.basename(r))

    if 'zpatches' in installed_themes:
        del installed_themes['zpatches']

    log.value(installed_themes)

    return installed_themes


def is_theme_supported(theme):
    log.message('Checking if the current theme is supported')

    current_theme = ''
    installed_themes = get_installed_themes()

    for pkg in installed_themes.values():
        if theme in pkg:
            for k, v in installed_themes.items():
                if set(v) == set(pkg):
                    current_theme = k
            break

    if current_theme in SUPPORTED:
        log.message(theme, ' is supported')
        return True

    log.message(theme, ' isn\'t supported')
    return False


def get_colors():
    log.message('Getting colors of the icons')

    colors = []
    is_provided = False
    package_settings = get_package_settings()
    pattern = re.compile('#([A-Fa-f0-9]{6})')
    options = ['color', 'color_on_hover', 'color_on_select']

    if package_settings.get('color'):
        for opt in options:
            color = package_settings.get(opt)

            if pattern.match(color):
                is_provided = True

                hex_color = color.lstrip('#')
                rgb_color = [
                    int(hex_color[i: i + 2], 16) for i in (0, 2, 4)
                ]

                color = ', '.join(str(e) for e in rgb_color)

                log.value('`', opt, '`: ', '[', color, ']')

                colors.append('\n    "layer0.tint": [' + color + '],')
            else:
                colors.append('')

        if is_provided:
            return colors

    return ''


def patch(theme, colors):
    log.message('Patching the current theme')

    dest = os.path.join(get_dest_path(), theme)

    with open(dest, 'w') as t:
        t.write(TEMPLATE % {
            'name': os.path.splitext(theme)[0],
            'color': colors[0],
            'color_on_hover': colors[1],
            'color_on_select': colors[2],
            'size': CURRENT_SETTINGS['size'],
            'opacity': CURRENT_SETTINGS['opacity'],
            'opacity_on_hover': CURRENT_SETTINGS['opacity_on_hover'],
            'opacity_on_select': CURRENT_SETTINGS['opacity_on_select']
        })
        t.close()


def activate():
    log.message('Activating the icons')

    theme = CURRENT_UI_THEME
    supported = is_theme_supported(theme)
    force_override = CURRENT_SETTINGS['force_override']

    if not supported or force_override:
        dest = get_dest_path()
        colors = get_colors()
        icons = os.path.join(dest, 'icons')
        multi = os.path.join(dest, 'multi')
        single = os.path.join(dest, 'single')
        patched = os.path.join(dest, theme)

        if colors:
            if os.path.isdir(single):
                log.message('Activating the single color mode')
                os.rename(icons, multi)
                os.rename(single, icons)
            else:
                log.message('The single color mode is already activated')
        else:
            if os.path.isdir(multi):
                log.message('Activating the multi color mode')
                os.rename(icons, single)
                os.rename(multi, icons)
            else:
                log.message('The multi color mode is already activated')

            colors = ['', '', '']

        if not os.path.isfile(patched) or SETTINGS_CHANGED:
            patch(theme, colors)
            log.warning('Please restart your Sulbime Text for these changes ',
                        'to take effect ...')
        else:
            log.message('The theme is already patched')
    else:
        clear()

    log.done()


def clear():
    log.message('Clearing patches of the supported themes')

    theme = get_sublime_settings().get('theme')
    path = os.path.join(get_dest_path(), theme)

    if is_theme_supported(theme) and os.path.isfile(path):
        os.remove(path)


def on_changed_sublime_settings():
    global CURRENT_UI_THEME
    global SETTINGS_CHANGED

    log.separator()
    log.message('The settings are changed')

    theme = get_sublime_settings().get('theme')

    if theme != CURRENT_UI_THEME:
        SETTINGS_CHANGED = True
        log.message('`theme` is changed')
        CURRENT_UI_THEME = theme

    if SETTINGS_CHANGED:
        log.message('Current theme')
        log.value(CURRENT_UI_THEME)
        activate()
        SETTINGS_CHANGED = False
    else:
        log.done()


def on_changed_package_settings():
    global CURRENT_SETTINGS
    global SETTINGS_CHANGED

    package_settings = get_package_settings()
    log.DEBUG = package_settings.get('debug')

    log.separator()
    log.message('The settings are changed')

    for k in CURRENT_SETTINGS.keys():
        if CURRENT_SETTINGS[k] != package_settings.get(k):
            SETTINGS_CHANGED = True
            log.message('`', k, '` is changed')
            CURRENT_SETTINGS[k] = package_settings.get(k)

    if SETTINGS_CHANGED:
        log.message('Current settings')
        log.value(CURRENT_SETTINGS)
        activate()
        SETTINGS_CHANGED = False
    else:
        log.done()


def init():
    global CURRENT_SETTINGS
    global CURRENT_UI_THEME

    package_settings = get_package_settings()
    sublime_settings = get_sublime_settings()

    log.DEBUG = package_settings.get('debug')

    log.separator()
    log.message('Initializing')

    log.message('Getting the current theme')
    CURRENT_UI_THEME = sublime_settings.get('theme')
    log.value(CURRENT_UI_THEME)

    log.message('Getting the current package settings')
    for k in CURRENT_SETTINGS.keys():
        CURRENT_SETTINGS[k] = package_settings.get(k)
    log.value(CURRENT_SETTINGS)

    sublime_settings.add_on_change('zzfiocss', on_changed_sublime_settings)
    package_settings.add_on_change('zzfiocps', on_changed_package_settings)


def plugin_loaded():
    init()
    activate()
