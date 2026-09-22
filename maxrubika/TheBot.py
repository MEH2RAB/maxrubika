import aiohttp
import asyncio
import json
import re
import logging
from aiohttp import web
from typing import Union, Any, Dict, Optional
import maxrubika
from .bot import Methods
from .bot.token import TokenString
from .bot.exceptions import (
    APIException, Network,
    Timeout, BadGateway,
    JSONDecode, ServerError,
    InvalidInput, InvalidAccess,
    TooRequests, TokenError
)
from .bot.registry import HandlerRegistry
from .bot.bridge import DecoratorBridge
from .types.incoming import Events
from .bot.plugin import PluginManager
from .data import Data

logger = logging.getLogger(__name__)

class Response(Data):
    pass

class Bot(Methods):
    TOKEN_PATTERN = re.compile(r'^[A-Z]{5}[0-9A-Z]{59}$')

    def __init__(
        self,
        token: Optional[str] = None,
        token_string: Optional[str] = None,
        password: Optional[str] = None,
        timeout: Union[int, float] = 30,
        max_retries: Union[int, float] = 5,
        show_welcome: bool = True
    ):
        """
        Initialize the Bot instance.

        Parameters:
            token (Optional[str]): Bot authentication token. If not provided
                or invalid, the bot will prompt for it via console input.
            token_string (Optional[str]): Encrypted TokenString. Takes priority over token.
            password (Optional[str]): Password for encrypted TokenString.
            timeout (int): Request timeout in seconds. Defaults to 30.
            max_retries (int): Maximum number of retry attempts on network
                errors. Defaults to 5.
            show_welcome (bool, optional): If True, show welcome message (default: True).
        """
        maxrubika.show_welcome_message(show_welcome)

        if token_string:
            token = TokenString(token_string).to_token(password)
            if not token:
                raise TokenError(
                "Invalid token_string or wrong password.")
        elif not token or not self.TOKEN_PATTERN.match(token.strip()):
            token = self._get_token()

        self.token = token
        self.timeout = float(timeout)
        self.max_retries = int(max_retries)
        self.base_url = f"https://botapi.rubika.ir/v3/{token}"

        self._registry = HandlerRegistry(self)
        self._bridge = DecoratorBridge(self._registry)
        self.plugin_manager = PluginManager(self)

        self._connector: Optional[aiohttp.TCPConnector] = None
        self._session: Optional[aiohttp.ClientSession] = None

    def _get_token(self) -> str:
        while True:
            token = input("Enter your bot token: ").strip()
            if self.TOKEN_PATTERN.match(token):
                return token
            print("Invalid token format. Try again.")

    def __getattr__(self, name: str):
        if name in (
            'on_new_message', 'on_edit_message', 'on_delete_message', 'on_message',
            'on_callback', 'on_command', 'middleware',
            'on_start', 'on_shutdown'
        ):
            return getattr(self._bridge, name)
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            if self._connector is None or self._connector.closed:
                self._connector = aiohttp.TCPConnector(ssl=False, limit=20)

            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(
                timeout=timeout,
                connector=self._connector
            )
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
        if self._connector and not self._connector.closed:
            await self._connector.close()

    def disconnect(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.close())
            else:
                loop.run_until_complete(self.close())
        except RuntimeError:
            asyncio.run(self.close())

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}/{endpoint}"
        session = await self._get_session()

        last_error = None

        for attempt in range(self.max_retries):
            try:
                async with session.request(method.upper(), url, **kwargs) as resp:
                    text = (await resp.text()).strip()

                    if resp.status == 502:
                        raise BadGateway(
                            dev_message=f"Server returned 502"
                        )

                    if resp.status == 500:
                        raise ServerError(
                            dev_message=f"Server returned error"
                        )

                    if resp.status >= 400:
                        raise APIException(
                            status=f"HTTP_{resp.status}",
                            dev_message=f"HTTP {resp.status}: {text[:500]}"
                        )

                    try:
                        data = json.loads(text)
                    except json.JSONDecodeError as e:
                        raise JSONDecode(
                            dev_message=f"Failed to parse JSON response. Raw: {text[:200]}"
                        ) from e

                    if isinstance(data, dict):
                        api_status = data.get('status', '')
                        error_message = data.get('dev_message')

                        if api_status != 'OK':
                            if api_status == 'SERVER_ERROR':
                                raise ServerError(dev_message=error_message)
                            elif api_status == 'INVALID_INPUT':
                                raise InvalidInput(dev_message=error_message)
                            elif api_status == 'INVALID_ACCESS':
                                raise InvalidAccess(dev_message=error_message)
                            elif api_status == 'TOO_REQUESTS':
                                raise TooRequests(dev_message=error_message)
                            elif api_status == 'ERROR':
                                raise APIException(status=api_status, dev_message=error_message)
                            elif api_status == 'Timeout':
                                raise Timeout(dev_message=error_message)
                            else:
                                raise APIException(status=api_status, dev_message=error_message)

                    return Response(data)

            except (BadGateway, ServerError, Timeout) as e:
                if attempt < self.max_retries - 1:
                    wait = 2 ** attempt
                    logger.warning(f"Request failed - Attempt {attempt + 1}/{self.max_retries}: {type(e).__name__}")
                    await asyncio.sleep(wait)
                    continue
                raise

            except (JSONDecode, InvalidInput, InvalidAccess, TooRequests, APIException) as e:
                raise

            except Exception as e:
                last_error = e
                logger.warning(f"Request failed - Attempt {attempt + 1}/{self.max_retries}: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue

        if last_error:
            raise Network(
                dev_message=f"Request failed after {self.max_retries} attempts."
            ) from last_error
        else:
            raise Network(
                dev_message=f"Failed to call {endpoint} after {self.max_retries} attempts."
            )

    def _parse_raw_update(self, raw: Dict[str, Any]) -> "Events":
        update_type = raw.get('type', '')
        chat_id = raw.get('chat_id', '')

        envelope = Events(data=raw, bot=self)

        envelope.update_type = update_type
        envelope.chat_id = chat_id
        envelope.timestamp = raw.get('update_time')

        if update_type == 'NewMessage':
            envelope.message = raw.get('new_message')
        elif update_type == 'UpdatedMessage':
            envelope.edited_message = raw.get('updated_message')
        elif update_type == 'RemovedMessage':
            envelope.deleted_message_id = str(raw.get('removed_message_id', ''))
        elif update_type == 'InlineMessage':
            envelope.callback_payload = raw

        return envelope

    async def _handle_webhook(self, request: web.Request) -> web.Response:
        try:
            data = await request.json()
        except json.JSONDecodeError:
            logger.error("Invalid JSON received in webhook")
            return web.json_response({"status": "ERROR"}, status=400)

        if "inline_message" in data:
            raw = data["inline_message"]
            raw["type"] = "InlineMessage"
            event = self._parse_raw_update(raw)
            asyncio.create_task(self._registry.feed(event))

        elif "update" in data:
            event = self._parse_raw_update(data["update"])
            asyncio.create_task(self._registry.feed(event))

        return web.json_response({"status": "OK"})