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

    def plugin_loaded():
        settings.init()
        icons.init()

    def plugin_unloaded():
        settings.clear_listener()

        from package_control import events

        if events.pre_upgrade(PACKAGE_NAME) or events.remove(PACKAGE_NAME):
            cleaning.clean_all()
else:
    raise ImportWarning("Doesn't support Sublime Text versions prior to 3114")
