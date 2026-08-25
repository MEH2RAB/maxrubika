from typing import Optional, Union, Literal
import logging
from . import Messenger
from .client.exceptions import PlatformError

class Shad(Messenger):
    VALID_SHAD_PLATFORMS = ('shad_web', 'shad_pwa', 'shad_android')
    
    def __init__(
        self,
        session: Optional[str] = None,
        auth: Optional[str] = None,
        private_key: Optional[Union[str, bytes]] = None,
        timeout: Union[str, int, float] = 30,
        proxy: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        platform: Literal['shad_web', 'shad_pwa', 'shad_android'] = 'shad_web',
        api_version: Literal[5, 6] = 6,
        max_retries: int = 5,
        stop_on_first_match: bool = False,
        continue_on_error: bool = True
    ) -> None:
        """
        Initialize the Shad client.

        Parameters:
            session (str, optional): Session file name or path.
            auth (str, optional): Authentication key (32 lowercase letters).
            private_key (str or bytes, optional): RSA private key.
            timeout (int or float, optional): Request timeout in seconds (default: 30).
            proxy (str, optional): Proxy address (example: 'http://127.0.0.1:80').
            logger (logging.Logger, optional): Logger instance.
            platform (Literal['shad_web', 'shad_pwa', 'shad_android']): Shad platform (default: 'shad_web').
            api_version (Literal[5, 6]): API version to use (default: 6).
            max_retries (int, optional): Maximum number of retries (default: 5).
            stop_on_first_match (bool, optional): Stop on first handler match.
            continue_on_error (bool, optional): Continue on auth errors.

        Raises:
            PlatformError: If platform is not one of 'shad_web', 'shad_pwa', or 'shad_android'.
        """
        if platform not in self.VALID_SHAD_PLATFORMS:
            raise PlatformError(
                f"Invalid Shad platform '{platform}'. Valid platforms are: {', '.join(self.VALID_SHAD_PLATFORMS)}"
            )

        super().__init__(
            session=session,
            auth=auth,
            private_key=private_key,
            timeout=timeout,
            proxy=proxy,
            logger=logger,
            platform=platform,
            api_version=api_version,
            max_retries=max_retries,
            stop_on_first_match=stop_on_first_match,
            continue_on_error=continue_on_error
        )