import threading
import asyncio
import inspect
from typing import Dict, Optional, List
import aiohttp
import logging
import maxrubika
from ...types import Event
from ..exceptions import (NetworkError, StopHandler, ServerError)

def capitalize(text: str) -> str:
    return "".join(word.title() for word in text.split("_"))

class Api:
    HEADERS = {
        "content-type": "application/json",
        "connection": "keep-alive",
    }

    def __init__(self, client: "maxrubika.Client") -> None:
        self.client = client
        self.max_retries = client.max_retries
        self.logger = logging.getLogger(__name__)
        self.headers = self.HEADERS.copy()
        self.headers["user-agent"] = client.user_agent

        platform = client.DEFAULT_PLATFORM["platform"]
        if platform == "Web":
            self.headers["origin"] = "https://web.rubika.ir"
            self.headers["referer"] = "https://web.rubika.ir/"
        elif platform == "Android":
            self.headers.pop("origin", None)
            self.headers.pop("referer", None)
            self.headers["user-agent"] = "okhttp/3.12.1"
        else:
            self.headers["origin"] = "https://m.rubika.ir"
            self.headers["referer"] = "https://m.rubika.ir/"

        connector = aiohttp.TCPConnector(verify_ssl=False, limit=100)
        self.session = aiohttp.ClientSession(
            connector=connector,
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(total=client.timeout),
        )

        self.api_url = None
        self.wss_url = None
        self.ws = None

        self.api_map: Dict[str, str] = {}
        self.api_priority: List[str] = []
        self._api_code_by_url: Dict[str, str] = {}

    @staticmethod
    def _normalize_url(url: Optional[str]) -> Optional[str]:
        if not url:
            return None
        return url.rstrip("/")

    @staticmethod
    def _ensure_trailing_slash(url: str) -> str:
        return url if not url or url.endswith("/") else f"{url}/"

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    async def get_dcs(self, max_retries: int = 3, backoff: float = 1.0) -> bool:
        url = "https://getdcmess.iranlms.ir/"
        for attempt in range(max_retries):
            try:
                async with self.session.get(url, proxy=self.client.proxy) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    data = json_data.get("data", {})
                    api_list = data.get("API", {})
                    socket_list = data.get("socket", {})

                    self.api_map = {}
                    for code, endpoint in api_list.items():
                        if not endpoint:
                            continue
                        normalized_code = str(code)
                        normalized_endpoint = self._ensure_trailing_slash(endpoint.rstrip("/"))
                        self.api_map[normalized_code] = normalized_endpoint

                    self._api_code_by_url = {
                        self._normalize_url(url): code
                        for code, url in self.api_map.items()
                        if self._normalize_url(url)
                    }

                    preferred_codes = []
                    default_api_code = data.get("default_api")
                    if default_api_code is not None:
                        default_api_code = str(default_api_code)

                    default_apis = data.get("default_apis") or []
                    for code in default_apis:
                        code_str = str(code)
                        if code_str in self.api_map and code_str not in preferred_codes:
                            preferred_codes.append(code_str)

                    if (
                        default_api_code
                        and default_api_code in self.api_map
                        and default_api_code not in preferred_codes
                    ):
                        preferred_codes.insert(0, default_api_code)

                    if not preferred_codes:
                        preferred_codes = list(self.api_map.keys())

                    self.api_priority = preferred_codes
                    self.api_url = self.api_map.get(self.api_priority[0]) if self.api_priority else None

                    self.wss_url = socket_list.get(data.get("default_socket"))

                    if self.api_url and self.wss_url:
                        return True
                    else:
                        raise ServerError("Server returned incomplete data.")

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                self.logger.warning(
                    f"Data Centers unreachable (attempt {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff * (2**attempt))

        raise NetworkError(
            "Could not reach Data Centers after multiple attempts."
        )

    async def _http_request(
        self,
        data: Dict,
        max_retries: int = 3,
        backoff: float = 1.0
    ) -> Optional[Dict]:

        candidates = []
        seen = set()

        def add(url_str):
            if not url_str:
                return
            u = url_str.rstrip("/")
            if u not in seen:
                seen.add(u)
                candidates.append(u)
        
        add(self.api_url)
        for code in self.api_priority:
            add(self.api_map.get(code))
        for endpoint in self.api_map.values():
            add(endpoint)
        
        for candidate in candidates:
            for attempt in range(max_retries):
                try:
                    async with self.session.post(
                        candidate, json=data, proxy=self.client.proxy
                    ) as response:
                        response.raise_for_status()
                        code = self._api_code_by_url.get(candidate)
                        if code:
                            if code in self.api_priority:
                                self.api_priority.remove(code)
                            self.api_priority.insert(0, code)
                            self.api_url = self.api_map.get(code, candidate)
                        return await response.json()
                except Exception as e:
                    self.logger.warning(
                        f"{candidate} request failed (attempt {attempt + 1}/{max_retries}): {e}"
                    )
                    if attempt < max_retries - 1:
                        await asyncio.sleep(backoff * (2 ** attempt))
        
        self.logger.error(f"Request failed after exhausting all {len(candidates)} endpoints.")
        return None

    async def handle_update(self, name: str, event: dict) -> None:
        for func, handler in self.client.handlers.items():
            try:
                if isinstance(handler, type):
                    handler = handler()

                if handler.__name__ != capitalize(name):
                    continue

                event_obj = Event(event.copy())

                if not await handler(event=event_obj):
                    continue

                handler_executed = False
                if not inspect.iscoroutinefunction(func):
                    if self.client.stop_on_first_match:
                        await asyncio.to_thread(func, event_obj)
                    else:
                        threading.Thread(target=func, args=(event_obj,)).start()
                    handler_executed = True
                else:
                    if self.client.stop_on_first_match:
                        await func(event_obj)
                    else:
                        asyncio.create_task(func(event_obj))
                    handler_executed = True

                if handler_executed and self.client.stop_on_first_match:
                    break
            except StopHandler:
                break
            except Exception as e:
                self.logger.error(
                    f"Handler '{name}' failed: {e}",
                    extra={"data": event}  
                )