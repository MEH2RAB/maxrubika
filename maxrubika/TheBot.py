import aiohttp
import asyncio
import json
import re
from aiohttp import web
from typing import Union, Any, Dict, Optional
from .bot import Methods
from .bot.exceptions import (
    APIException,
    Network,
    Timeout,
    BadGateway,
    JSONDecode,
    ServerError,
    InvalidInput,
    InvalidAccess,
    TooRequests
)
from .bot.registry import HandlerRegistry
from .bot.bridge import DecoratorBridge
from .types.incoming import IncomingEnvelope
from .bot.plugin import PluginManager

class Response:
    def __init__(self, data: dict):
        self._data = data
        self.original_update = data

    def __str__(self) -> str:
        return self.jsonify(indent=2)

    def __getattr__(self, name):
        if name in self._data:
            value = self._data[name]
            if isinstance(value, dict):
                return Response(value)
            elif isinstance(value, list):
                return [Response(item) if isinstance(item, dict) else item for item in value]
            return value

        if 'data' in self._data and isinstance(self._data['data'], dict):
            if name in self._data['data']:
                value = self._data['data'][name]
                if isinstance(value, dict):
                    return Response(value)
                elif isinstance(value, list):
                    return [Response(item) if isinstance(item, dict) else item for item in value]
                return value

        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def jsonify(self, indent: int = None) -> str:
        return json.dumps(
            self._data,
            indent=indent,
            ensure_ascii=False,
            default=str
        )

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def to_dict(self) -> dict:
        return self._data

class Bot(Methods):
    TOKEN_PATTERN = re.compile(r'^[A-Z]{5}[0-9A-Z]{59}$')

    def __init__(
        self,
        token: Optional[str] = None,
        timeout: Union[int, float] = 20,
        max_retries: Union[int, float] = 5
    ):
        """
        Initialize the Bot instance.

        Parameters:
            token (Optional[str]): Bot authentication token. If not provided
                or invalid, the bot will prompt for it via console input.
            timeout (int): Request timeout in seconds. Defaults to 20.
            max_retries (int): Maximum number of retry attempts on network
                errors or server failures. Defaults to 5.
        """
        if not token or not self.TOKEN_PATTERN.match(token.strip()):
            token = self._get_token()

        self.token = token
        self.timeout = float(timeout)
        self.max_retries = int(max_retries)
        self.base_url = f"https://botapi.rubika.ir/v3/{token}"

        self._registry = HandlerRegistry(self)
        self._bridge = DecoratorBridge(self._registry)
        self.plugin_manager = PluginManager(self)

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
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    async def _request(self, method: str, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}/{endpoint}"
        timeout = aiohttp.ClientTimeout(total=self.timeout)

        last_error = None
        last_error_type = None

        for attempt in range(self.max_retries):
            try:
                connector = aiohttp.TCPConnector(ssl=False, limit=100)
                async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                    async with session.request(method.upper(), url, **kwargs) as resp:
                        text = (await resp.text()).strip()

                        if resp.status == 502:
                            print(f"502 Bad Gateway attempt {attempt + 1}/{self.max_retries}")
                            if attempt < self.max_retries - 1:
                                await asyncio.sleep(2 ** attempt)
                                continue
                            else:
                                raise BadGateway(
                                    dev_message=f"Server returned 502 after {self.max_retries} attempts."
                                )

                        if resp.status == 500:
                            print(f"500 Internal Server Error attempt {attempt + 1}/{self.max_retries}")
                            if attempt < self.max_retries - 1:
                                await asyncio.sleep(2 ** attempt)
                                continue
                            else:
                                raise ServerError(
                                    dev_message=f"Server returned 500 after {self.max_retries} attempts."
                                )

                        if resp.status >= 400:
                            print(f"HTTP {resp.status} attempt {attempt + 1}/{self.max_retries}")
                            if attempt < self.max_retries - 1 and resp.status in [429, 503, 504]:
                                await asyncio.sleep(2 ** attempt)
                                continue
                            else:
                                raise APIException(
                                    status=f"HTTP_{resp.status}",
                                    dev_message=f"HTTP {resp.status}: {text[:500]}"
                                )

                        try:
                            data = json.loads(text)
                        except json.JSONDecodeError as e:
                            print(f"JSON Error attempt {attempt + 1}/{self.max_retries}")
                            if attempt < self.max_retries - 1:
                                await asyncio.sleep(2 ** attempt)
                                continue
                            else:
                                raise JSONDecode(
                                    dev_message=f"Failed to parse JSON response. Raw: {text[:200]}"
                                )

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
                                    raise APIException(
                                        status=api_status,
                                        dev_message=error_message
                                    )
                                elif api_status == 'Timeout':
                                    if attempt < self.max_retries - 1:
                                        print(f"API Timeout attempt {attempt + 1}/{self.max_retries}")
                                        await asyncio.sleep(2 ** attempt)
                                        continue
                                    else:
                                        raise Timeout(dev_message=error_message)
                                else:
                                    raise APIException(
                                        status=api_status,
                                        dev_message=error_message
                                    )

                        return Response(data)

            except (BadGateway, JSONDecode, ServerError, InvalidInput, InvalidAccess, TooRequests, Timeout):
                raise

            except APIException:
                raise

            except asyncio.TimeoutError as e:
                last_error = e
                last_error_type = 'timeout'
                print(f"Timeout attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue

            except aiohttp.ClientConnectionError as e:
                last_error = e
                last_error_type = 'connection'
                print(f"Connection error attempt {attempt + 1}/{self.max_retries}: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue

            except Exception as e:
                last_error = e
                last_error_type = 'unknown'
                print(f"Unknown error attempt {attempt + 1}/{self.max_retries}: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue

        if last_error_type == 'timeout':
            raise Timeout(
                dev_message=f"Request timed out after {self.max_retries} attempts."
            ) from last_error

        elif last_error_type == 'connection':
            raise Network(
                dev_message=f"Connection failed after {self.max_retries} attempts."
            ) from last_error

        elif last_error:
            raise APIException(
                status="ERROR",
                dev_message=f"Request failed after {self.max_retries} attempts."
            ) from last_error

        else:
            raise APIException(
                status="UNKNOWN_ERROR",
                dev_message=f"Failed to call {endpoint} after {self.max_retries} attempts."
            )

    def _parse_raw_update(self, raw: Dict[str, Any]) -> "IncomingEnvelope":
        update_type = raw.get('type', '')
        chat_id = raw.get('chat_id', '')

        envelope = IncomingEnvelope(
            update_type=update_type,
            chat_id=chat_id,
            bot=self,
            timestamp=raw.get('update_time'),
            original_data=raw,
        )

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