import os
import re
import sublime
import sublime_plugin

from collections import OrderedDict

from ..common import settings
from ..common.templates.theme import TEMPLATE as THEMETPL
from ..common.utils import path
from ..common.utils.logging import log, dump, warning

PATTERN = re.compile(r"^Packages/|\/.*$")
COLORTPL = "\n    \"layer0.tint\": {},"


def _patch_general(themes, dest, icostgs):
    color = icostgs.get("color", "")
    color_on_hover = icostgs.get("color_on_hover", "")
    color_on_select = icostgs.get("color_on_select", "")

    for theme in themes:
        theme_dest = os.path.join(dest, theme)
        theme_name = os.path.splitext(theme)[0]
        log("Patching `{}`".format(theme))

        with open(theme_dest, "w") as t:
            t.write(THEMETPL % {
                "name": theme_name,
                "color": COLORTPL.format(color) if color else color,
                "color_on_hover": COLORTPL.format(color_on_hover)
                if color_on_hover else color_on_hover,
                "color_on_select": COLORTPL.format(color_on_select)
                if color_on_select else color_on_select,
                "size": icostgs.get("size", ""),
                "opacity": icostgs.get("opacity", ""),
                "opacity_on_hover": icostgs.get("opacity_on_hover", ""),
                "opacity_on_select": icostgs.get("opacity_on_select", "")
            })
            t.close()


def _patch_specific(themes, dest, icostgs):
    pass


def _clean_patches(patches):
    log("Clearing old unnecessary patches")
    try:
        for patch in patches:
            if os.path.exists(patch):
                os.remove(patch)
    except Exception as error:
        log("Error during patch cleaning")
        dump(error)


def get_current():
    log("Getting the current theme")

    current = settings.subltxt().get("theme")
    dump(current)

    return current


def get_installed(logging=True):
    if logging:
        log("Getting installed themes")

    theme_resources = sublime.find_resources("*.sublime-theme")
    all_themes_ordered = OrderedDict([])
    installed_themes = {}

    for res in theme_resources:
        package = re.sub(PATTERN, "", res)
        all_themes_ordered[package] = []

    for res in theme_resources:
        package = re.sub(PATTERN, "", res)
        theme = os.path.basename(res)

        all_themes_ordered[package].append(theme)

    for k in all_themes_ordered.keys():
        value = all_themes_ordered[k]
        is_addon = False
        is_patch = True if k == settings.OVERLAY_ROOT else False

        for v in installed_themes.values():
            if set(value).issubset(set(v)):
                is_addon = True

        if not (is_addon or is_patch):
            installed_themes[k] = value

    if logging:
        dump(installed_themes)

    return installed_themes


def get_customizable():
    log("Getting the list of theme packages with customization support")

    installed_themes = get_installed(logging=False)
    customizable_themes = []

    # TODO: Clean up in 3.1.0
    prev_res = sublime.find_resources(".st-file-icons")
    curr_res = sublime.find_resources(".supports-a-file-icon-customization")
    theme_res = prev_res + curr_res

    for res in theme_res:
        pkg = re.sub(PATTERN, "", res)

        if pkg in installed_themes:
            customizable_themes.append(pkg)

    dump(customizable_themes)

    return customizable_themes


class AfiPatchThemesCommand(sublime_plugin.ApplicationCommand):
    def run(self, overwrite=False):
        log("Preparing to patch")

        installed_themes = get_installed()
        customizable_themes = get_customizable()
        icons_settings = settings.icons()
        force_mode = settings.package().get("force_mode")

        general_to_patch = []
        patches_to_clean = []

        general = path.get_overlay_patches_general()
        general_multi = os.path.join(general, "multi")
        general_single = os.path.join(general, "single")
        general_new = general_multi
        general_old = general_single

        if "color" in icons_settings and icons_settings["color"]:
            general_new = general_single
            general_old = general_multi

        for pkg in installed_themes:
            for theme in installed_themes[pkg]:
                old = os.path.join(general_old, theme)
                new = os.path.join(general_new, theme)

                if pkg in customizable_themes and not force_mode:
                    if os.path.exists(old):
                        patches_to_clean.append(old)

                    if os.path.exists(new):
                        patches_to_clean.append(new)
                else:
                    if not os.path.exists(new) or overwrite:
                        general_to_patch.append(theme)

                    if os.path.exists(old):
                        patches_to_clean.append(old)

        _clean_patches(patches_to_clean)

        if general_to_patch:
            try:
                _patch_general(general_to_patch, general_new, icons_settings)
                log("Patching finished successfully")
            except Exception as error:
                log("Error during patching")
                dump(error)
            else:
                sublime.run_command("refresh_folder_list")
                warning()
        else:
            log("All the themes are already patched")
