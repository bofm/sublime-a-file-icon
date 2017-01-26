import json
import os
import shutil
import sublime
import tempfile
import zipfile

from ..common import settings
from ..common.utils import path
from ..common.utils.logging import log, dump

from . import themes


def _create_dirs():
    log("Creating directories")

    try:
        g = path.get_overlay_patches_general()
        s = path.get_overlay_patches_specific()

        if not os.path.exists(g):
            os.makedirs(g)

            if not os.path.exists(s):
                os.makedirs(s)
    except Exception as error:
        log("Error during create")
        dump(error)


def _get_icons_path(package_name):
    package_path = "Packages/" + package_name
    for res in sublime.find_resources("file_type_default.png"):
        if res.startswith(package_path):
            return os.path.dirname(res)
    return False


def _extract_general():
    log("Extracting general icons")

    temp_dir = tempfile.mkdtemp()
    dest_path = path.get_overlay_patches_general()

    try:
        with zipfile.ZipFile(path.get_package_archive(), "r") as z:
            members = z.namelist()
            members_to_extract = [m for m in members if m.startswith("icons")]

            z.extractall(temp_dir, members_to_extract)

            shutil.move(os.path.join(temp_dir, "icons", "single"), dest_path)
            shutil.move(os.path.join(temp_dir, "icons", "multi"), dest_path)
    except Exception as error:
        log("Error during extract")
        dump(error)


def _copy_general():
    log("Copying general icons")

    package_path = path.get_package_icons()
    general_path = path.get_overlay_patches_general()

    src_multi = os.path.join(package_path, "multi")
    src_single = os.path.join(package_path, "single")

    dest_multi = os.path.join(general_path, "multi")
    dest_single = os.path.join(general_path, "single")

    try:
        shutil.copytree(src_multi, dest_multi)
        shutil.copytree(src_single, dest_single)
    except Exception as error:
        log("Error during copy")
        dump(error)


def _copy_specific():
    log("Checking theme specific icons")

    customizable_themes = themes.get_customizable()
    general_path = path.get_overlay_patches_general()
    specific_path = path.get_overlay_patches_specific()

    src_multi = os.path.join(general_path, "multi")
    src_single = os.path.join(general_path, "single")

    pkgicons = json.loads(sublime.load_resource("Packages/" +
                                                settings.PACKAGE_NAME +
                                                "/common/icons.json"))
    allicons = sublime.find_resources("*.png")

    try:
        for theme in customizable_themes:
            theme_patch_path = os.path.join(specific_path, theme)
            theme_patch_multi_path = os.path.join(theme_patch_path, "multi")
            theme_patch_single_path = os.path.join(theme_patch_path, "single")

            if not os.path.exists(theme_patch_path):
                log("Copying `{}` specific icons".format(theme))

                os.makedirs(theme_patch_path)
                os.makedirs(theme_patch_multi_path)
                os.makedirs(theme_patch_single_path)

                theme_icons_path = _get_icons_path(theme)
                theme_icons = [
                    os.path.basename(os.path.splitext(i)[0])
                    for i in allicons if i.startswith(theme_icons_path)
                ]

                for icon in pkgicons:
                    if icon not in theme_icons:
                        for filename in os.listdir(src_multi):
                            if filename.startswith(icon):
                                shutil.copy(
                                    os.path.join(src_multi, filename),
                                    theme_patch_multi_path
                                )

                        for filename in os.listdir(src_single):
                            if filename.startswith(icon):
                                shutil.copy(
                                    os.path.join(src_single, filename),
                                    theme_patch_single_path
                                )
    except Exception as error:
        log("Error during copy")
        dump(error)
    finally:
        sublime.run_command("afi_patch_themes")


def provide():
    if settings.is_package_archive():
        _extract_general()
    else:
        _copy_general()

    _copy_specific()


def check():
    log("Checking icons")

    if not os.path.exists(path.get_overlay()):
        _create_dirs()
        sublime.set_timeout_async(provide, 0)
    else:
        sublime.set_timeout_async(_copy_specific, 0)
        dump("All the necessary icons are provided")
