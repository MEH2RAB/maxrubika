import random
import logging
from typing import Optional, Literal, Union, TYPE_CHECKING

from .rubino import Methods

if TYPE_CHECKING:
    import maxrubika

class Rubino(Methods):
    RUBINO_URLS = [f'https://rubinog2c{i}.iranlms.ir/' for i in range(0, 86) if i != 3]

    def __init__(
        self,
        session: Optional[str] = None,
        string_session: Optional[str] = None,
        password: Optional[str] = None,
        auth: Optional[str] = None,
        client: Optional["maxrubika.Messenger"] = None,
        timeout: Union[str, int, float] = 30,
        proxy: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        platform: Literal['web', 'pwa', 'android', 'ios', 'rubx', 'rubikids', 'rubino', 'tv_android', 'tv_web', 'vod_web'] = 'rubino',
        api_version: Literal[0, 1] = 1,
        max_retries: int = 5,
        as_dict: bool = False,
        show_welcome: bool = True
    ):
        """
        Initialize the Rubino client.

        Parameters:
            session (str, optional): Session file name or path.
            string_session (str, optional): StringSession string. Takes priority over 'session'.
            password (str, optional): Password for encrypted StringSession.
            auth (str, optional): Authentication key.
            client (Messenger, optional): Pre-built Messenger instance.
            timeout (int or float, optional): Request timeout in seconds (default: 30).
            proxy (str, optional): Proxy address (example: 'http://127.0.0.1:80').
            logger (logging.Logger, optional): Logger instance.
            platform: Client platform (default: 'rubino').
            api_version (int): API version (0 for plain, 1 for encrypted). Defaults to 1.
            max_retries (int, optional): Maximum number of retries (default: 5).
            as_dict (bool, optional): If True, return responses as plain dict (default: False).
            show_welcome (bool, optional): If True, show welcome message (default: True).
        """
        import maxrubika
        from .rubino.exceptions import InvalidInput, InvalidAccess, InvalidSession, InvalidAuthInput
        from .data import Data

        maxrubika.show_welcome_message(show_welcome)

        if api_version not in (0, 1):
            raise InvalidInput("'api_version' must be 0 or 1.")

        if api_version == 0:
            raise InvalidAccess(
                "API version 0 is not ready yet. Please use api_version=1."
            )

        self.api_version = api_version
        self.as_dict = as_dict
        self._Data = Data

        provided = sum([bool(session), bool(string_session), bool(auth), bool(client)])
        if provided == 0:
            raise InvalidInput(
                "One of 'session', 'string_session', 'auth', or 'client' must be provided."
            )
        if provided > 1:
            raise InvalidInput(
                "Only one of 'session', 'string_session', 'auth', or 'client' should be provided."
            )

        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(__name__)

        self.logger = logger
        self.rubino_url = None
        self.failed_count = 0
        self.max_retries = max_retries
        self.profile_id = "" if api_version == 1 else None
        self._owns_client = False
        self._auth = auth
        self._client = None

        if session:
            if not isinstance(session, str):
                raise InvalidSession()
            self._client = maxrubika.Messenger(
                session,
                timeout=timeout,
                proxy=proxy,
                logger=logger,
                max_retries=max_retries,
                platform=platform,
                show_welcome=False
            )
            self._owns_client = True
        elif string_session:
            if not isinstance(string_session, str):
                raise InvalidSession()
            self._client = maxrubika.Messenger(
                string_session=string_session,
                password=password,
                timeout=timeout,
                proxy=proxy,
                logger=logger,
                max_retries=max_retries,
                platform=platform,
                show_welcome=False
            )
            self._owns_client = True
        elif client:
            if not hasattr(client, 'auth'):
                raise InvalidAuthInput()
            self._client = client

    @property
    def auth(self):
        return self._auth or (self._client.auth if self._client else None)

    def __enter__(self):
        if self._client and self._owns_client:
            self._client.__enter__()
        self._verify()
        return self

    def __exit__(self, *args):
        if self._client and self._owns_client:
            self._client.__exit__(*args)

    async def __aenter__(self):
        if self._client and self._owns_client:
            await self._client.__aenter__()
        await self._verify_a()
        return self

    async def __aexit__(self, *args):
        if self._client and self._owns_client:
            await self._client.__aexit__(*args)

    def _verify(self):
        me = self.get_me()

        if isinstance(me, dict):
            me = self._Data(me)

        profiles = me.find_keys('profiles') or []

        for p in profiles:
            p_data = self._Data(p) if isinstance(p, dict) else p

            if self.api_version == 1:
                if p_data.find_keys('owner_type') == 'Main':
                    self.profile_id = p_data.find_keys('id')
                    return
            else:
                if p_data.find_keys('is_default'):
                    self.profile_id = p_data.find_keys('id')
                    return

    async def _verify_a(self):
        me = await self.get_me()

        if isinstance(me, dict):
            me = self._Data(me)

        profiles = me.find_keys('profiles') or []

        for p in profiles:
            p_data = self._Data(p) if isinstance(p, dict) else p

            if self.api_version == 1:
                if p_data.find_keys('owner_type') == 'Main':
                    self.profile_id = p_data.find_keys('id')
                    return
            else:
                if p_data.find_keys('is_default'):
                    self.profile_id = p_data.find_keys('id')
                    return

    def _pick_url(self):
        self.rubino_url = random.choice(self.RUBINO_URLS)
        self.failed_count = 0

    def _next_url(self):
        self.failed_count += 1
        if self.failed_count >= self.max_retries:
            self._pick_url()