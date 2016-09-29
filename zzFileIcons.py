# -*- coding: utf-8 -*-

import sublime
import os
import re

'''Should be such as theme name in Package Control'''
SUPPORTED = [
    'Boxy Theme'
]

PACKAGE_SETTINGS = 'zzFileIcons.sublime-settings'
SUBLIME_SETTINGS = 'Preferences.sublime-settings'

CURRENT_UI_THEME = ''
CURRENT_SETTINGS = {
    'color': '',
    'default_opacity': '',
    'hovered_opacity': '',
    'selected_opacity': '',
    'force_override': ''
}

DIR = 'zzFileIcons'
DEBUG = False
NEED_PATCH = False

TEMPLATE = '''
// %(name)s Theme Overlay
// ============================================================================

[
  // Sidebar File Icons
  // --------------------------------------------------------------------------

  // Default

  {
    "class": "icon_file_type",
    "layer0.opacity": %(default_opacity)s,%(color)s
    "content_margin": [8, 8]
  },

  // Hovered

  {
    "class": "icon_file_type",
    "parents": [{"class": "tree_row", "attributes": ["hover"]}],
    "layer0.opacity": %(hovered_opacity)s
  },

  // Selected

  {
    "class": "icon_file_type",
    "parents": [{"class": "tree_row", "attributes": ["selected"]}],
    "layer0.opacity": %(selected_opacity)s
  }
]
'''


def get_sublime_settings():
    return sublime.load_settings(SUBLIME_SETTINGS)


def get_package_settings():
    return sublime.load_settings(PACKAGE_SETTINGS)


def log_msg(*args):
    if DEBUG:
        text = ['zzFileIcons: ']
        for arg in args:
            text.append(str(arg))
        print(''.join(text))


def log_val(*args):
    if DEBUG:
        text = ['         >>> ']
        for arg in args:
            text.append(str(arg))
        print(''.join(text))


def log_sep():
    if DEBUG:
        print('\n***\n')


def get_dest_path():
    return os.path.join(sublime.packages_path(), DIR, 'zzicons')


def get_installed_themes():
    log_msg('Getting installed themes')

    installed_themes = {}

    for r in sublime.find_resources('*.sublime-theme'):
        installed_themes.setdefault(os.path.basename(os.path.dirname(r)),
                                    []).append(os.path.basename(r))

    if 'zzicons' in installed_themes:
        del installed_themes['zzicons']

    log_val(installed_themes)

    return installed_themes


def is_theme_supported(theme):
    log_msg('Checking if current theme is supported')

    current_theme = ''
    installed_themes = get_installed_themes()

    for pkg in installed_themes.values():
        if theme in pkg:
            for k, v in installed_themes.items():
                if set(v) == set(pkg):
                    current_theme = k
            break

    if current_theme in SUPPORTED:
        log_msg(theme, ' is supported')
        return True

    log_msg(theme, ' isn\'t supported')
    return False


def get_color():
    log_msg('Getting color of the icons')

    color = get_package_settings().get('color', '')
    pattern = re.compile('#([A-Fa-f0-9]{6})')

    if pattern.match(color):
        hex_color = color.lstrip('#')
        rgb_color = [
            int(hex_color[i: i + 2], 16) for i in (0, 2, 4)
        ]

        color = ', '.join(str(e) for e in rgb_color)

        log_val('[', color, ']')

        return '\n    "layer0.tint": [' + color + '],'

    return ''


def patch(theme, color):
    global NEED_PATCH

    package_settings = get_package_settings()

    dest = os.path.join(get_dest_path(), theme)

    if not os.path.isfile(dest):
        NEED_PATCH = True

    if NEED_PATCH:
        log_msg('Patching the current theme')
        default_opacity = package_settings.get('default_opacity', 0.75)
        hovered_opacity = package_settings.get('hovered_opacity', 1.0)
        selected_opacity = package_settings.get('selected_opacity', 1.0)

        with open(dest, 'w') as t:
            t.write(TEMPLATE % {
                'name': os.path.splitext(theme)[0],
                'color': color,
                'default_opacity': default_opacity,
                'hovered_opacity': hovered_opacity,
                'selected_opacity': selected_opacity
            })
            t.close()

        NEED_PATCH = False

    log_msg('Done')


def activate():
    log_msg('Activating icons')

    theme = get_sublime_settings().get('theme')
    supported = is_theme_supported(theme)
    force_override = get_package_settings().get('force_override')

    if not supported or force_override:
        dest = get_dest_path()
        color = get_color()
        icons = os.path.join(dest, 'icons')
        multi = os.path.join(dest, 'multi')
        single = os.path.join(dest, 'single')

        if color and os.path.isdir(single):
            log_msg('Activating single mode')
            os.rename(icons, multi)
            os.rename(single, icons)
        elif not color and os.path.isdir(multi):
            log_msg('Activating multi mode')
            os.rename(icons, single)
            os.rename(multi, icons)

        patch(theme, color)
    else:
        clear()


def clear():
    log_msg('Clearing patches of the supported themes')

    theme = get_sublime_settings().get('theme')
    path = os.path.join(get_dest_path(), theme)

    if is_theme_supported(theme) and os.path.isfile(path):
        os.remove(path)


def on_changed_sublime_settings():
    log_sep()
    log_msg('Sublime settings are changed')

    global CURRENT_UI_THEME
    global NEED_PATCH

    theme = get_sublime_settings().get('theme')

    if theme != CURRENT_UI_THEME:
        log_msg('`theme` is changed')
        NEED_PATCH = True

        log_msg('Current theme')
        CURRENT_UI_THEME = theme
        log_val(CURRENT_UI_THEME)

        activate()


def on_changed_package_settings():
    log_sep()
    log_msg('Package settings are changed')

    global CURRENT_SETTINGS
    global DEBUG
    global NEED_PATCH

    package_settings = get_package_settings()

    for k in CURRENT_SETTINGS.keys():
        if CURRENT_SETTINGS[k] != package_settings.get(k):
            log_msg('`', k, '` is changed')
            NEED_PATCH = True

            log_msg('Current settings')
            CURRENT_SETTINGS[k] = package_settings.get(k)
            log_val(CURRENT_SETTINGS)

            activate()

            break

    DEBUG = package_settings.get('debug')


def init():
    global CURRENT_SETTINGS
    global CURRENT_UI_THEME
    global DEBUG

    package_settings = get_package_settings()
    sublime_settings = get_sublime_settings()

    DEBUG = package_settings.get('debug')

    log_sep()
    log_msg('Initializing')

    log_msg('Getting the current theme')
    CURRENT_UI_THEME = sublime_settings.get('theme')
    log_val(CURRENT_UI_THEME)

    log_msg('Getting the current package settings')
    for k in CURRENT_SETTINGS.keys():
        CURRENT_SETTINGS[k] = package_settings.get(k)
    log_val(CURRENT_SETTINGS)

    sublime_settings.add_on_change('zzfiocss', on_changed_sublime_settings)
    package_settings.add_on_change('zzfiocps', on_changed_package_settings)


def plugin_loaded():
    init()
    activate()
