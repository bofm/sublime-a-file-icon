import sublime

if int(sublime.version()) > 3113:
    from .common import settings
    from .common.utils import cleaning

    from .core import icons
    from .core import aliases

    from .common.settings import PACKAGE_NAME
    from .common.utils.environment import AfiEnvironmentCommand
    from .common.utils.changelog import AfiChangelogCommand
    from .common.utils.reloader import AfiReloadListener
    from .common.utils.reloader import AfiReloadCommand
    from .common.utils.cleaning import AfiCleanCommand
    from .common.utils.cleaning import AfiRevertCommand

    from .core.aliases import AfiCheckAliasesCommand
    from .core.themes import AfiPatchThemesCommand

    def init():
        settings.init()
        icons.init()

    def prepare():
        start_msg = "{}: Preparing to configure the plugin. ".format(
            PACKAGE_NAME
        ) + "Do not close the Sublime Text."

        done_msg = "{}: Done.".format(PACKAGE_NAME)

        print(start_msg)

        window = sublime.active_window()
        view = window.active_view()

        def cleanup():
            view.erase_status("afi")

        def reload():
            sublime.run_command("afi_reload")
            view.set_status("afi", done_msg)
            sublime.set_timeout(cleanup, 1000)

        view.set_status("afi", start_msg)

        sublime.set_timeout_async(reload, 5000)

    def plugin_loaded():
        from package_control import events

        if events.post_upgrade(PACKAGE_NAME) or events.install(PACKAGE_NAME):
            prepare()
        else:
            init()

    def plugin_unloaded():
        settings.clear_listener()

        from package_control import events

        if events.pre_upgrade(PACKAGE_NAME) or events.remove(PACKAGE_NAME):
            cleaning.clean_all()
else:
    raise ImportWarning("Doesn't support Sublime Text versions prior to 3114")
