from typing import Optional, Union, Literal
import asyncio
import os
import logging
import re
from rich.console import Console
from rich.text import Text
import maxrubika
from .client import Methods
from .client.core.cipher import Cipher
from .client.core.session import Session, StringSession
from .client.exceptions import (
    ApiVersionError,
    PlatformError,
    AuthError,
    TimeoutError,
    MaxRetriesError,
    ProxyError,
    SessionError
)
from .client.core.configs import DEFAULT_PLATFORM, PLATFORMS, VALID_PLATFORMS, USER_AGENT

class Client(Methods):
    USER_AGENT = USER_AGENT
    API_VERSION = 6

    def __init__(
        self,
        session: Optional[str] = None,
        string_session: Optional[str] = None,
        password: Optional[str] = None,
        auth: Optional[str] = None,
        private_key: Optional[Union[str, bytes]] = None,
        timeout: Union[str, int, float] = 30,
        proxy: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        platform: Literal['web', 'pwa', 'android', 'rubx', 'rubikids', 'rubino'] = 'web',
        api_version: Literal[5, 6] = 6,
        max_retries: int = 5,
        stop_on_first_match: bool = False,
        continue_on_error: bool = True,
        show_welcome: bool = True
    ) -> None:
        """
        Initialize the Rubika client.

        Parameters:
            session (str, optional): Session file name or path. (api_version=6 only)
            string_session (str, optional): StringSession string. Takes priority over 'session'.
            password (str, optional): Password for encrypted StringSession. Required if StringSession was created with a password.
            auth (str, optional): Authentication key.
            private_key (str or bytes, optional): RSA private key. (api_version=6 only)
            timeout (int or float, optional): Request timeout in seconds (default: 30).
            proxy (str, optional): Proxy address (example: 'http://127.0.0.1:80').
            logger (logging.Logger, optional): Logger instance.
            platform: Literal['web', 'pwa', 'android', 'rubx', 'rubikids', 'rubino']: Client platform (default: 'web').
            api_version: Literal[5, 6]: API version to use (default: 6).
                - 6: Requires 'auth' + 'private_key' (or 'session').
                - 5: Requires only 'auth'.
            max_retries (int, optional): Maximum number of retries for requests (default: 5).
            stop_on_first_match (bool, optional): If True, stop processing handlers after the first match (default: False).
            continue_on_error (bool, optional): If True, continue trying other platforms on auth errors (default: True).
            show_welcome (bool, optional): If True, show welcome message (default: True).

        Raises:
            ApiVersionError: If api_version is invalid.
            PlatformError: If platform is invalid.
            AuthError: If auth parameters are invalid.
            TimeoutError: If timeout is invalid.
            MaxRetriesError: If max_retries is invalid.
            ProxyError: If proxy is invalid.
            SessionError: If session or string_session is invalid.
        """
        maxrubika.show_welcome_message(show_welcome)

        if type(self) is Client:
            err_console = Console(stderr=True)
            warning_msg = Text()
            warning_msg.append("DeprecationWarning: ", style="bright_red")
            warning_msg.append("'Client'", style="bright_red underline")
            warning_msg.append(" is deprecated. Use ", style="bright_red")
            warning_msg.append("'Messenger'", style="bright_green underline")
            warning_msg.append(" instead.\n", style="bright_red")
            err_console.print(warning_msg)
        super().__init__()

        if api_version not in (5, 6):
            raise ApiVersionError("'api_version' must be 5 or 6.")

        self.API_VERSION = api_version

        if platform.lower() not in VALID_PLATFORMS:
            raise PlatformError(
                f"Invalid platform '{platform}'. Valid platforms are: {', '.join(VALID_PLATFORMS)}"
            )

        if api_version == 6:
            if session is None and string_session is None and (auth is None or private_key is None):
                raise AuthError("API v6 requires: 'session', 'string_session', OR both 'auth' and 'private_key'.")
            if auth is not None and private_key is None:
                raise AuthError("If 'auth' is provided, 'private_key' must also be provided.")
            if private_key is not None and auth is None:
                raise AuthError("If 'private_key' is provided, 'auth' must also be provided.")
        elif api_version == 5:
            if auth is None:
                raise AuthError("API v5 requires: 'auth'.")
            if private_key is not None:
                raise AuthError("API v5 does not support 'private_key'.")
            session = None
            string_session = None

        if auth is not None:
            if not isinstance(auth, str):
                raise AuthError("The 'auth' parameter must be a string.")
            if not re.match(r'^[a-z]{32}$', auth):
                raise AuthError("The 'auth' must be 32 lowercase letters only.")

        if isinstance(timeout, bool):
            raise TimeoutError("'timeout' must be a number, not a boolean.")
        try:
            timeout = float(timeout)
        except (TypeError, ValueError):
            raise TimeoutError("The 'timeout' parameter must be a number.")
        if timeout <= 0:
            raise TimeoutError("'timeout' must be greater than 0.")

        if isinstance(max_retries, bool) or not isinstance(max_retries, int):
            raise MaxRetriesError("'max_retries' must be an integer.")
        if max_retries < 0:
            raise MaxRetriesError("'max_retries' must be >= 0.")

        if proxy is not None and not isinstance(proxy, str):
            raise ProxyError("'proxy' must be a string.")

        self.DEFAULT_PLATFORM = DEFAULT_PLATFORM.copy()
        self.DEFAULT_PLATFORM.update(PLATFORMS.get(platform.lower(), {}))
        self._original_platform = platform.lower()

        if session is not None:
            if not isinstance(session, str):
                raise SessionError("The 'session' parameter must be a string.")
            self.session_name = os.path.basename(session)
            self.session_path = session
            session = Session(session)

        elif string_session is not None:
            try:
                session = Session(string_session=string_session, password=password)
                info = session.information()
                if info:
                    auth = info[1]
                    private_key = info[4]
                    self.session_name = f"maxrubika_{auth[:10]}"
                    self.session_path = self.session_name
            except ValueError:
                raise SessionError(
                    "String session is invalid or wrong password."
                ) from None

        else:
            self.session_name = f"maxrubika_{auth[:10]}" if auth else None
            self.session_path = self.session_name
            session = Session(self.session_name) if self.session_name else None

        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(__name__)

        if isinstance(private_key, str):
            if not private_key.startswith('-----BEGIN RSA PRIVATE KEY-----'):
                private_key = f'-----BEGIN RSA PRIVATE KEY-----\n{private_key}'
            if not private_key.endswith('-----END RSA PRIVATE KEY-----'):
                private_key += '\n-----END RSA PRIVATE KEY-----'

        self.auth = auth
        self.logger = logger
        self.private_key = private_key
        self.user_agent = self.USER_AGENT
        self.timeout = timeout
        self.session = session
        self.proxy = proxy
        self.decode_auth = None
        self.import_key = None
        self.guid = None
        self.key = None
        self.handlers = {}
        self.max_retries = max_retries
        self.stop_on_first_match = stop_on_first_match
        self.continue_on_error = continue_on_error

    def __del__(self) -> None:
        try:
            self.disconnect()
        except:
            pass

    def __enter__(self) -> "Client":
        if not getattr(self, 'connection', None):
            return self.start()
        return self

    def __exit__(self, *args, **kwargs):
        try:
            self.disconnect()
        except Exception:
            pass

    async def __aenter__(self) -> "Client":
        if not getattr(self, 'connection', None):
            return await self.start()
        return self

    async def __aexit__(self, *args, **kwargs):
        try:
            await self.close()
        except Exception:
            pass

    async def stop(self) -> None:
        if hasattr(self, 'connection'):
            if self.connection.session.closed:
                return
        await self.close()

class Messenger(Client):
    pass