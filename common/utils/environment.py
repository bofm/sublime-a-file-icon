import json
import os
import sublime
import sublime_plugin

from .. import settings
from ...core.themes import get_current, get_installed


def _get_package_version():
    pkg_json = sublime.load_resource("Packages/" + settings.PACKAGE_NAME +
                                     "/package.json")

    return json.loads(pkg_json)["version"]


def _is_installed_via_pc():
    return str(settings.PACKAGE_NAME in set(settings.pkgctrl()
                                            .get("installed_packages", [])))


class AfiEnvironmentCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        info = {}

        info["platform"] = sublime.platform()
        info["sublime_version"] = sublime.version()

        info["current_theme"] = get_current()
        info["installed_themes"] = "".join([
            "<li>{}</li>".format(k) for k in get_installed().keys()
        ])

        info["package_version"] = _get_package_version()
        info["installed_via_pc"] = _is_installed_via_pc()

        msg = """\
            <b>Platform:</b> %(platform)s
            <b>A File Icon:</b> %(package_version)s
            <b>Sublime Text:</b> %(sublime_version)s
            <b>Package Control:</b> %(installed_via_pc)s
            <b>Current Theme:</b> %(current_theme)s
            <b>Installed Themes:</b>
            <ul>
            %(installed_themes)s
            </ul>
        """ % info

        view = sublime.active_window().active_view()

        def copy_and_hide(msg):
            sublime.set_clipboard(msg.replace("    ", ""))
            view.hide_popup()

        view.show_popup("<style>ul { margin: 0;}</style>" +
                        "<a href=\"" + msg + "\">Copy</a><br><br>" +
                        msg.replace("\n", "<br>").replace("    ", ""),
                        on_navigate=copy_and_hide)
