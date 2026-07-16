from typing import Optional, Union, Literal
import asyncio
import logging
import re
import maxrubika
from .client import Methods
from .client.core.session import Session
from .client.exceptions import InvalidInput

class Client(Methods):
    DEFAULT_PLATFORM = {
        'app_name': 'Main',
        'app_version': '4.4.33',
        'platform': 'Web',
        'package': 'web.rubika.ir',
    }

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/150.0.7871.115 Safari/537.36"
    )

    API_VERSION = '6'

    def __init__(
        self,
        session: Optional[str] = None,
        auth: Optional[str] = None,
        private_key: Optional[Union[str, bytes]] = None,
        timeout: Union[str, int, float] = 30,
        proxy: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        platform: Literal['web', 'pwa', 'android'] = 'web',
        max_retries: int = 5,
        stop_on_first_match: bool = False
    ) -> None:
        """
        Initialize the Rubika client.

        Parameters:
            session (str, optional): Session file name or path.
            auth (str, optional): Authentication key (required with private_key).
            private_key (str or bytes, optional): RSA private key (required with auth).
            timeout (int or float, optional): Request timeout in seconds (default: 30).
            proxy (str, optional): Proxy address (example: 'http://127.0.0.1:80').
            logger (logging.Logger, optional): Logger instance.
            platform: Literal['web', 'pwa', 'android']: Client platform (default: 'web').
            max_retries (int, optional): Maximum number of retries for requests (default: 5).
            stop_on_first_match (bool, optional): If True, stop processing handlers after the first match (default: False).

        Raises:
            ValueError: If any input is invalid.
            TypeError: If the 'session' parameter is not a string.
        """
        super().__init__()

        if session is None and auth is None and private_key is None:
            raise InvalidInput(
                "No authentication method provided. You must either:"
                " 1. Provide 'session' parameter for session-based authentication."
                " 2. Provide both 'auth' and 'private_key' for direct authentication"
            )

        if auth is not None and private_key is None:
            raise InvalidInput(
            "If 'auth' is provided, 'private_key' must also be provided."
            )
        if private_key is not None and auth is None:
            raise InvalidInput(
            "If 'private_key' is provided, 'auth' must also be provided."
            )

        if auth is not None:
            if not isinstance(auth, str):
                raise InvalidInput("The 'auth' parameter must be a string.")
            if not re.match(r'^[a-z]{32}$', auth):
                raise InvalidInput("The 'auth' must be 32 lowercase letters only.")

        self.DEFAULT_PLATFORM = self.DEFAULT_PLATFORM.copy()
        self.DEFAULT_PLATFORM['lang_code'] = 'fa'
        
        if platform.lower() == 'pwa':
            self.DEFAULT_PLATFORM['platform'] = 'PWA'
            self.DEFAULT_PLATFORM['app_version'] = '2.5.8'
            self.DEFAULT_PLATFORM['package'] = 'm.rubika.ir'
        elif platform.lower() == 'android':
            self.DEFAULT_PLATFORM['platform'] = 'Android'
            self.DEFAULT_PLATFORM['app_version'] = '4.0.5'
            self.DEFAULT_PLATFORM['package'] = 'app.rbmain.a'

        if not isinstance(timeout, (int, float)):
            try:
                timeout = float(timeout)
            except (ValueError, TypeError):
                raise InvalidInput("The 'timeout' parameter must be a number.")

        if session is not None:
            if not isinstance(session, str):
                raise InvalidInput("The 'session' parameter must be a string.")
            self.session_name = session
            session = Session(session)
        else:
            self.session_name = f"maxrubika_{auth[:10]}"
            session = Session(self.session_name)

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
        self.is_sync = False
        self.guid = None
        self.key = None
        self.handlers = {}
        self.max_retries = max_retries
        self.stop_on_first_match = stop_on_first_match

        try:
            asyncio.get_running_loop()
        except RuntimeError:
            self.start()

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
            await self.disconnect()
        except Exception:
            pass

    async def stop(self) -> None:
        if self.connection.session.closed:
            return
        await self.disconnect()