import asyncio
import json
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

CLIENT_INFO = {
    'app_name': 'Main',
    'app_version': '4.1.1',
    'lang_code': 'fa',
    'package': 'app.rbmain.a',
    'platform': 'Android',
    'temp_code': '30',
    'store': 'Direct'
}

class Request:
    async def request(
        self: "maxrubika.Rubino",
        method: str,
        input: dict = None
    ):
        """
        Send a request to the Rubino API.

        Parameters:
            method (str): The API method name to call.
            input (dict, optional): The input data to send with the request.
                In api_version=1, 'profile_id' in input is used internally
                and NOT sent to the API inside input.

        Returns:
            The parsed response data on success.
        """
        import aiohttp
        from ..data import Data
        from .exceptions import raise_exception, NetworkError
        from .crypto import Crypto

        api_version = self.api_version

        input_data = dict(input or {})

        if api_version == 1:
            profile_id = input_data.pop('profile_id', None) or self.profile_id
        else:
            profile_id = self.profile_id

        if not self.rubino_url:
            self._pick_url()

        total_urls = len(self.RUBINO_URLS)

        for url_index in range(total_urls):
            last_error = None

            for attempt in range(self.max_retries):
                try:
                    auth = self.auth

                    if api_version == 1:
                        inner_data = {
                            "client": self._client.DEFAULT_PLATFORM if self._client else CLIENT_INFO,
                            "method": method,
                            "profile_id": profile_id,
                            "is_background": False,
                            "input": input_data
                        }

                        data_enc = Crypto.encrypt_auth(
                            json.dumps(inner_data, ensure_ascii=False),
                            auth
                        )

                        data = {
                            "api_version": "1",
                            "auth": auth,
                            "data_enc": data_enc,
                            "sign": None
                        }
                    else:
                        data = {
                            "api_version": "0",
                            "auth": auth,
                            "client": self._client.DEFAULT_PLATFORM if self._client else {},
                            "data": input_data,
                            "method": method
                        }

                    if self._client and hasattr(self._client, 'connection') and self._client.connection:
                        session = self._client.connection.session
                        proxy = self._client.proxy
                    else:
                        connector = aiohttp.TCPConnector(verify_ssl=False)
                        session = aiohttp.ClientSession(
                            connector=connector,
                            timeout=aiohttp.ClientTimeout(total=30)
                        )
                        proxy = None

                    try:
                        async with session.post(
                            self.rubino_url,
                            json=data,
                            proxy=proxy
                        ) as response:
                            if response.status == 502:
                                raise aiohttp.ClientConnectionError("Bad Gateway (502)")
                            result = await response.json()
                    finally:
                        if not (self._client and hasattr(self._client, 'connection') and self._client.connection):
                            await session.close()

                    if api_version == 1 and result.get("data_enc"):
                        plain = Crypto.decrypt_auth(result["data_enc"], auth)
                        obj = json.loads(plain)

                        result["data"] = obj.get("data")
                        result["status"] = obj.get("status")
                        result["status_det"] = obj.get("status_det")

                    if result.get('status') == 'OK':
                        self.failed_count = 0
                        data_result = result.get('data', {})

                        if getattr(self, 'as_dict', False):
                            return data_result

                        return Data(data_result)

                    raise_exception(result.get('status_det'), result)

                except asyncio.TimeoutError as e:
                    last_error = e
                    self.logger.warning(
                        f"Timeout on {self.rubino_url} "
                        f"(attempt {attempt + 1}/{self.max_retries})"
                    )
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(2 ** attempt)

                except Exception as e:
                    error_msg = str(e).lower()
                    if any(keyword in error_msg for keyword in
                           ['timeout', 'connection', 'bad gateway', 'server error', '502', '503', '504']):
                        last_error = e
                        self.logger.warning(
                            f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}"
                        )
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(2 ** attempt)
                        self.failed_count += 1
                    else:
                        raise

            if url_index < total_urls - 1:
                self._pick_url()
                self.failed_count = 0

        raise NetworkError(
            f"All {total_urls} Rubino URLs exhausted. "
            f"Last error: {last_error}"
        )