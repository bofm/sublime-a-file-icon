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


def get_dest_path():
    return os.path.join(sublime.packages_path(), DIR, 'zzicons')


def get_installed_themes():
    installed_themes = {}

    for r in sublime.find_resources('*.sublime-theme'):
        installed_themes.setdefault(os.path.basename(os.path.dirname(r)),
                                    []).append(os.path.basename(r))

    if 'zzicons' in installed_themes:
        del installed_themes['zzicons']

    return installed_themes


def is_theme_supported(theme):
    current_theme = ''
    installed_themes = get_installed_themes()

    for pkg in installed_themes.values():
        if theme in pkg:
            for k, v in installed_themes.items():
                if set(v) == set(pkg):
                    current_theme = k
            break

    if current_theme in SUPPORTED:
        return True

    return False


def get_color():
    color = get_package_settings().get('color', '')
    pattern = re.compile('#([A-Fa-f0-9]{6})')

    if pattern.match(color):
        hex_color = color.lstrip('#')
        rgb_color = [
            int(hex_color[i: i + 2], 16) for i in (0, 2, 4)
        ]

        color = ', '.join(str(e) for e in rgb_color)

        return '\n    "layer0.tint": [' + color + '],'

    return ''


def patch():
    global NEED_PATCH

    sublime_settings = get_sublime_settings()
    package_settings = get_package_settings()

    theme = sublime_settings.get('theme')

    dest = os.path.join(get_dest_path(), theme)

    if not os.path.isfile(dest):
        NEED_PATCH = True

    if NEED_PATCH:
        color = get_color()
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


def activate():
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
            os.rename(icons, multi)
            os.rename(single, icons)
        elif not color and os.path.isdir(multi):
            os.rename(icons, single)
            os.rename(multi, icons)

        patch()
    else:
        clear()


def clear():
    theme = get_sublime_settings().get('theme')
    path = os.path.join(get_dest_path(), theme)

    if is_theme_supported(theme) and os.path.isfile(path):
        os.remove(path)


def on_changed_sublime_settings():
    global CURRENT_UI_THEME
    global NEED_PATCH

    theme = get_sublime_settings().get('theme')

    if theme != CURRENT_UI_THEME:
        NEED_PATCH = True
        activate()
        CURRENT_UI_THEME = theme


def on_changed_package_settings():
    global CURRENT_SETTINGS
    global NEED_PATCH

    package_settings = get_package_settings()

    for k in CURRENT_SETTINGS.keys():
        if CURRENT_SETTINGS[k] != package_settings.get(k):
            NEED_PATCH = True
            activate()
            CURRENT_SETTINGS[k] = package_settings.get(k)


def init():
    global CURRENT_SETTINGS
    global CURRENT_UI_THEME

    package_settings = get_package_settings()
    sublime_settings = get_sublime_settings()

    CURRENT_UI_THEME = sublime_settings.get('theme')

    for k in CURRENT_SETTINGS.keys():
        CURRENT_SETTINGS[k] = package_settings.get(k)

    sublime_settings.add_on_change('zzfiocss', on_changed_sublime_settings)
    package_settings.add_on_change('zzfiocps', on_changed_package_settings)


def plugin_loaded():
    init()
    activate()
