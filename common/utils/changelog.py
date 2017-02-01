import sublime
import sublime_plugin
import webbrowser

from .. import settings


class AfiChangelogCommand(sublime_plugin.WindowCommand):
    def on_navigate(self, href):
        webbrowser.open_new_tab(href)

    def run(self):
        view = self.window.new_file()
        view.set_name("{} – Changelog".format(settings.PACKAGE_NAME))
        view.settings().set("gutter", False)
        view.settings().set("line_numbers", False)
        view.settings().set("caret_extra_top", 0)
        view.settings().set("caret_extra_bottom", 0)
        view.settings().set("caret_extra_width", 0)

        html = str(sublime.load_resource(
            "Packages/{}/.sublime/CHANGELOG.html".format(settings.PACKAGE_NAME)
        ))

        view.add_phantom(
            "afi_changelog",
            sublime.Region(0),
            html,
            sublime.LAYOUT_INLINE,
            on_navigate=self.on_navigate
        )

        view.set_read_only(True)
        view.set_scratch(True)
