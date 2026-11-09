from importlib import import_module
from datetime import datetime

__author__ = "MEHRAB Farahmand"
__version__ = "1.18.0"

_welcome_shown = False
_update_checked = False

IMPORTS = {
    "Bot": (".TheBot", "Bot"),
    "bot": (".TheBot", "Bot"),
    "Client": (".TheClient", "Client"),
    "Messenger": (".TheClient", "Messenger"),
    "messenger": (".TheClient", "Messenger"),
    "Rubino": (".TheRubino", "Rubino"),
    "rubino": (".TheRubino", "Rubino"),
    "RubiAI": (".TheRubiAI", "RubiAI"),
    "RubiAi": (".TheRubiAI", "RubiAI"),
    "rubiai": (".TheRubiAI", "RubiAI"),
    "RubikaAI": (".TheRubiAI", "RubiAI"),
    "RubikaAi": (".TheRubiAI", "RubiAI"),
    "Shad": (".TheShad", "Shad"),
    "shad": (".TheShad", "Shad"),
    "RubikaTV": (".TV", "RubikaTV"),
    "rubikatv": (".TV", "RubikaTV"),
}

def __getattr__(name):
    item = IMPORTS.get(name)
    if item is None:
        available = ", ".join(sorted(IMPORTS.keys()))
        raise AttributeError(
            f"module {__name__!r} has no attribute {name!r}. Available: {available}"
        )

    module_name, attribute_name = item
    module = import_module(module_name, __name__)
    value = getattr(module, attribute_name)

    globals()[name] = value
    del IMPORTS[name]
    return value

def __dir__():
    return sorted(set(globals()) | set(IMPORTS))

__all__ = [
    "Bot", "bot", "Client", "Messenger", "messenger",
    "Rubino", "rubino", "RubiAI", "RubiAi", "rubiai", "RubikaAI", "RubikaAi",
    "Shad", "shad", "RubikaTV", "rubikatv",
    "show_welcome_message", "check_for_updates", "show_announcements",
    "__author__", "__version__"
]

def show_welcome_message(show_welcome=True):
    global _welcome_shown, _update_checked
    if show_welcome and not _welcome_shown:
        _welcome_shown = True

        from rich.console import Console
        from rich.text import Text

        console = Console()
        text = Text()
        text.append("Welcome to MAXRubika library for Rubika & Shad Platforms", style="bold magenta")
        text.append(f"\nCopyright © {datetime.now().year} MAXRubika Team - All rights reserved.", style="cyan")
        text.append("\nGithub: ", style="white")
        text.append("https://github.com/MEH2RAB/maxrubika", style="green underline")
        text.append("\nChannel: ", style="white")
        text.append("https://Rubika.ir/TheMAXRubika", style="bright_blue underline")
        text.append("\nDocument: ", style="white")
        text.append("https://MEH2RAB.GitHub.io/maxrubika\n", style="yellow underline")
        console.print(text)

    if not _update_checked:
        _update_checked = True
        check_for_updates(__version__)

def check_for_updates(current_version_str):
    try:
        import json
        from urllib.request import Request, urlopen

        url = "https://mirror.max-server.ir/maxrubika/version"
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 Chrome/130.0.0.0 Mobile Safari/537.36"}

        req = Request(url, headers=headers)
        with urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode("utf-8"))

        latest_version_str = data["version"]

        def parse_version(version):
            return tuple(map(int, version.split(".")))

        if parse_version(latest_version_str) > parse_version(current_version_str):
            from rich.console import Console
            from rich.text import Text

            update_console = Console(stderr=True)
            update_msg = Text()

            update_msg.append(
                f"A new version of MAXRubika is available! (v{current_version_str} → v{latest_version_str})\n",
                style="bold bright_red",
            )

            if (data.get("has_changes") and data.get("changelog") and not data.get("is_changelog_long")):
                update_msg.append("\nRelease Notes: ", style="bold bright_cyan")
                update_msg.append(data["changelog"] + "\n")

            update_msg.append("\nRun: ", style="white")
            update_msg.append("pip install maxrubika --upgrade\n", style="gold1")
            update_console.print(update_msg)

        show_announcements(data.get("announcements"))

    except Exception:
        pass

def show_announcements(announcements):
    if not announcements:
        return

    from rich.console import Console
    from rich.text import Text

    console = Console(stderr=True)
    msg = Text()
    msg.append("Notices:\n", style="bold bright_cyan")
    for item in announcements:
        msg.append(f"● {item}\n")
    console.print(msg)