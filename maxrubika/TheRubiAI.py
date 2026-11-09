import logging
from typing import Optional, Union, Literal, TYPE_CHECKING

from .rubiai import Methods

if TYPE_CHECKING:
    import maxrubika

class RubiAI(Methods):
    def __init__(
        self,
        session: Optional[str] = None,
        string_session: Optional[str] = None,
        password: Optional[str] = None,
        auth: Optional[str] = None,
        client: Optional["maxrubika.Messenger"] = None,
        timeout: Union[int, float] = 30,
        proxy: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        platform: Literal['web', 'pwa', 'android', 'ios', 'rubx', 'rubikids', 'rubino', 'tv_android', 'tv_web', 'vod_web'] = 'ios',
        max_retries: int = 5,
        as_dict: bool = False,
        show_welcome: bool = True
    ):
        """
        Initialize a RubiAI instance.

        Parameters:
            session (str, optional): Session file name or path.
            string_session (str, optional): StringSession string. Takes priority over 'session'.
            password (str, optional): Password for encrypted StringSession.
            auth (str, optional): Authentication key.
            client (Messenger, optional): Pre-built Messenger instance.
            timeout (int or float, optional): Request timeout in seconds (default: 30).
            proxy (str, optional): Proxy address (example: 'http://127.0.0.1:80').
            logger (logging.Logger, optional): Logger instance.
            platform: Client platform (default: 'ios').
            max_retries (int, optional): Maximum number of retries (default: 5).
            as_dict (bool, optional): If True, return responses as plain dict (default: False).
            show_welcome (bool, optional): If True, show welcome message (default: True).
        """
        import maxrubika
        from .rubiai.exceptions import InvalidInput

        maxrubika.show_welcome_message(show_welcome)

        if client is not None:
            if not isinstance(client, (maxrubika.Client, maxrubika.Messenger)):
                message = "'client' must be an instance of 'maxrubika.Client' or 'maxrubika.Messenger'."
                raise InvalidInput(message)
            self.client = client
            self._owns_client = False
            self._auth = None
        elif session or string_session:
            self.client = maxrubika.Messenger(
                session=session,
                string_session=string_session,
                password=password,
                proxy=proxy,
                logger=logger,
                platform=platform,
                show_welcome=False,
            )
            self._owns_client = True
            self._auth = None
        elif auth:
            self.client = None
            self._owns_client = False
            self._auth = auth
        else:
            message = "One of 'session', 'string_session', 'auth', or 'client' must be provided."
            raise InvalidInput(message)

        self.base_url = "https://rubichat1.iranlms.ir/"
        self.max_retries = max_retries
        self.timeout = timeout
        self.as_dict = as_dict
        self.logger = (
            logging.getLogger(__name__)
            if not isinstance(logger, logging.Logger)
            else logger
        )
        self.client_info = {
            "app_name": "Main",
            "app_version": "4.1.0",
            "package": "app.rbmain.a",
            "platform": "Android"
        }

    @property
    def auth(self):
        return self._auth or (self.client.auth if self.client else None)

    def __enter__(self):
        if self._owns_client and self.client is not None:
            self.client.__enter__()
        return self

    def __exit__(self, *args):
        if self._owns_client and self.client is not None:
            self.client.__exit__(*args)

    async def __aenter__(self):
        if self._owns_client and self.client is not None:
            await self.client.__aenter__()
        return self

    async def __aexit__(self, *args):
        if self._owns_client and self.client is not None:
            await self.client.__aexit__(*args)