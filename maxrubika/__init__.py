import json
import sys
import builtins
from urllib.request import urlopen
from datetime import datetime

from rich.console import Console
from rich.text import Text

from .TheBot import Bot
from .TheClient import Client, Messenger

__author__ = "MEHRAB Farahmand"
__version__ = "1.8.0"

console = Console(stderr=True)

_BLOCKED_LIBRARIES = {"rubka", "pyrubi", "fast_rub", "rubigram", "rubikabot", "aiorubi", "rubkey", "rubpy", "roboka", "arsein"}
_original_import = builtins.__import__

def _get_root_module(name):
    return name.split(".", 1)[0]

def _print_blocked_error(names):
    error_msg = Text()
    error_msg.append("MAXRubika cannot run with incompatible libraries!\n", style="bold bright_red")
    error_msg.append("\nDetected: ", style="white")
    error_msg.append(", ".join(sorted(names)), style="bold yellow")
    error_msg.append("\n\nPlease remove the incompatible library from your project and\nrun MAXRubika again.", style="bright_magenta")
    console.print(error_msg)
    sys.exit(1)

def _check_already_imported():
    found = set()
    for module_name in sys.modules:
        root = _get_root_module(module_name)
        if root in _BLOCKED_LIBRARIES:
            found.add(root)
    if found:
        _print_blocked_error(found)

def _maxrubika_import(name, globals=None, locals=None, fromlist=(), level=0):
    root = _get_root_module(name)
    if level == 0 and root in _BLOCKED_LIBRARIES:
        _print_blocked_error({root})
    return _original_import(name, globals, locals, fromlist, level)

def check_for_updates(current_version_str):
    try:
        with urlopen("https://pypi.org/pypi/maxrubika/json", timeout=1) as response:
            data = json.loads(response.read().decode())
            latest_version_str = data["info"]["version"]

        def parse_version(v_str):
            return tuple(map(int, v_str.split(".")))

        if parse_version(latest_version_str) > parse_version(current_version_str):
            update_console = Console(stderr=True)
            update_msg = Text()
            update_msg.append(f"A new version of MAXRubika is available! (v{current_version_str} → v{latest_version_str})\n", style="bold bright_red")
            update_msg.append("   Run: ", style="white")
            update_msg.append("pip install maxrubika --upgrade\n", style="gold1")
            update_console.print(update_msg)
    except Exception:
        pass

console = Console()
text = Text()
text.append("Welcome to MAXRubika library for Rubika Platform", style="bold magenta")
text.append(f"\nCopyright © {datetime.now().year} MAXRubika Team - All rights reserved.", style="cyan")
text.append("\nGithub: ", style="white")
text.append("https://github.com/MEH2RAB/maxrubika", style="green underline")
text.append("\nChannel: ", style="white")
text.append("https://Rubika.ir/TheMAXRubika", style="bright_blue underline")
text.append("\nDocument: ", style="white")
text.append("https://MEH2RAB.GitHub.io/maxrubika\n", style="yellow underline")
console.print(text)

check_for_updates(__version__)

_check_already_imported()
builtins.__import__ = _maxrubika_import