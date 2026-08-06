import json
from urllib.request import urlopen
from datetime import datetime

from rich.console import Console
from rich.text import Text

from .TheBot import Bot
from .TheClient import Client, Messenger

__author__ = 'MEHRAB Farahmand'
__version__ = '1.6.0'

def check_for_updates(current_version_str):
    try:
        with urlopen("https://pypi.org/pypi/maxrubika/json", timeout=0.5) as response:
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
text.append("\nDocument: ", style="white")
text.append("https://MAXRubi.ir/documents\n", style="yellow underline")

console.print(text)

check_for_updates(__version__)