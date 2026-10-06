import re
import asyncio
from typing import Union, Optional
import aiohttp
from rich.console import Console

import maxrubika
from .bot import Methods
from .bot.session import Session
from .bot.updates import Updates
from .bot.token import TokenString
from .bot.exceptions import TokenError
from .bot.registry import HandlerRegistry
from .bot.bridge import DecoratorBridge
from .bot.plugin import PluginManager

console = Console(highlight=False)

class Bot(Session, Updates, Methods):
    TOKEN_PATTERN = re.compile(r'^[A-Z]{5}[0-9A-Z]{59}$')
    DEFAULT_BASE_URL = "https://botapi.rubika.ir/v3"

    def __init__(
        self,
        token: Optional[str] = None,
        token_string: Optional[str] = None,
        password: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Union[int, float] = 30,
        max_retries: Union[int, float] = 5,
        show_welcome: bool = True,
        run_all_handlers: bool = True
    ):
        """
        Initialize the Bot instance.

        Parameters:
            token (Optional[str]): Bot authentication token. If not provided
                or invalid, the bot will prompt for it via console input.
            token_string (Optional[str]): Encrypted TokenString. Takes priority over token.
            password (Optional[str]): Password for encrypted TokenString.
            base_url (str): Base API URL. Defaults to "https://botapi.rubika.ir/v3".
            timeout (int): Request timeout in seconds. Defaults to 30.
            max_retries (int): Maximum number of retry attempts on network
                errors. Defaults to 5.
            show_welcome (bool, optional): If True, show welcome message (default: True).
            run_all_handlers (bool, optional): If True (default), every handler whose
                constraints match an event is run, in registration order. If False,
                only the first matching handler runs, so registration order decides
                which handler wins.
        """
        maxrubika.show_welcome_message(show_welcome)

        self._session: Optional[aiohttp.ClientSession] = None
        self._close_task: Optional["asyncio.Task"] = None
        self._session_loop: Optional["asyncio.AbstractEventLoop"] = None

        if token_string:
            token = TokenString(token_string).to_token(password)
            if not token:
                raise TokenError(
                    "Invalid token_string or wrong password.")
        else:
            token = (token or "").strip()
            if not self.TOKEN_PATTERN.match(token):
                token = self._get_token()

        self.token = token
        self.timeout = float(timeout)
        self.max_retries = int(max_retries)
        self.base_url = f"{base_url.rstrip('/')}/{token}"
        self.run_all_handlers = bool(run_all_handlers)

        self._registry = HandlerRegistry(self)
        self._bridge = DecoratorBridge(self._registry)
        self.plugin_manager = PluginManager(self)

        for name in dir(type(self._bridge)):
            if name.startswith('_'):
                continue
            attr = getattr(type(self._bridge), name, None)
            if isinstance(attr, property):
                setattr(self, name, getattr(self._bridge, name))

    def _get_token(self) -> str:
        while True:
            console.print("Enter your bot token: ", style="bold yellow", end="")
            token = input().strip()
            if self.TOKEN_PATTERN.match(token):
                return token
            console.print("\nInvalid token format. Try again.\n", style="bold red")