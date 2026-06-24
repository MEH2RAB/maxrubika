from .TheBot import Bot
from . import types, hybrid

from colorama import init, Fore, Style
from datetime import datetime
import sys

init(autoreset=True, convert=True)

def print_with_color(text, color_style):
    sys.stdout.write(color_style + text + Style.RESET_ALL + "\n")
    sys.stdout.flush()

print_with_color("Welcome to MAXRubika library for Rubika Messenger", Fore.MAGENTA + Style.BRIGHT)
print_with_color(f"Copyright © {datetime.now().year} MEHRAB Farahmand - All rights reserved.", Fore.BLUE + Style.NORMAL)
print_with_color("Github: https://github.com/MEH2RAB/maxrubika", Fore.CYAN + Style.NORMAL)
print_with_color("Document: https://MAXRubi.ir\n", Fore.YELLOW + Style.NORMAL)

__author__ = 'MEHRAB Farahmand'
__version__ = '1.0.0'
__welcome__ = (f'Welcome to MAXRubika (version {__version__})\n')