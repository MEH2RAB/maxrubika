from typing import Optional, Union, Literal, TYPE_CHECKING
import logging

from . import Messenger

if TYPE_CHECKING:
    import maxrubika

class Shad(Messenger):
    PLATFORMS = ('shad_web', 'shad_pwa', 'shad_android')

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
        platform: Literal['shad_web', 'shad_pwa', 'shad_android'] = 'shad_web',
        api_version: Literal[5, 6] = 6,
        max_retries: int = 5,
        stop_on_first_match: bool = False,
        run_all_handlers: Optional[bool] = None,
        continue_on_error: bool = True,
        as_dict: bool = False,
        show_welcome: bool = True
    ):
        """
        Initialize the Shad client.

        Parameters:
            session (str, optional): Session file name or path. (api_version=6 only)
            string_session (str, optional): StringSession string. Takes priority over 'session'.
            password (str, optional): Password for encrypted StringSession.
            auth (str, optional): Authentication key (32 lowercase letters).
            private_key (str or bytes, optional): RSA private key. (api_version=6 only)
            timeout (int or float, optional): Request timeout in seconds (default: 30).
            proxy (str, optional): Proxy address (example: 'http://127.0.0.1:80').
            logger (logging.Logger, optional): Logger instance.
            platform (str): Shad platform (default: 'shad_web').
            api_version (int): API version to use (default: 6).
            max_retries (int, optional): Maximum number of retries (default: 5).
            stop_on_first_match (bool, optional): Deprecated. Use `run_all_handlers` instead.
            run_all_handlers (bool, optional): If True, run all matching handlers (default: True).
            continue_on_error (bool, optional): If True, continue on auth errors (default: True).
            as_dict (bool, optional): If True, return responses as plain dict (default: False).
            show_welcome (bool, optional): If True, show welcome message (default: True).

        Raises:
            PlatformError: If platform is not one of 'shad_web', 'shad_pwa', or 'shad_android'.
        """
        from .client.exceptions import PlatformError

        if platform not in self.PLATFORMS:
            raise PlatformError(
                f"Invalid Shad platform '{platform}'. Valid platforms are: {', '.join(self.PLATFORMS)}"
            )

        super().__init__(
            session=session,
            string_session=string_session,
            password=password,
            auth=auth,
            private_key=private_key,
            timeout=timeout,
            proxy=proxy,
            logger=logger,
            platform=platform,
            api_version=api_version,
            max_retries=max_retries,
            stop_on_first_match=stop_on_first_match,
            run_all_handlers=run_all_handlers,
            continue_on_error=continue_on_error,
            as_dict=as_dict,
            show_welcome=show_welcome
        )