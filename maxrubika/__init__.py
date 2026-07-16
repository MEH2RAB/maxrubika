from . import types, hybrid
from .TheClient import Client
from .TheBot import Bot

from rich.console import Console
from rich.text import Text
from datetime import datetime

__author__ = 'MEHRAB Farahmand'
__version__ = '1.3.0'

console = Console()

text = Text()
text.append("Welcome to MAXRubika library for Rubika Messenger", style="bold magenta")
text.append(f"\nCopyright © {datetime.now().year} MAXRubika Team - All rights reserved.", style="cyan")
text.append("\nGithub: ", style="white")
text.append("https://github.com/MEH2RAB/maxrubika", style="green underline")
text.append("\nDocument: ", style="white")
text.append("https://MAXRubi.ir/documents\n", style="yellow underline")

console.print(text)