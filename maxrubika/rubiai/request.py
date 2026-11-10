from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class Request:
    async def request(
        self: "maxrubika.RubiAI",
        method: str,
        input: Optional[Dict[str, Any]] = None
    ):
        """
        Send a normal HTTP request to the AI API.

        Parameters:
            method (str): Remote API method name.
            input (dict): Method-specific input parameters.

        Returns:
            The API output (wrapped in Data by default).
        """
        import asyncio
        import aiohttp
        from . import exceptions
        from ..data import Data

        if input is None:
            input = {}

        payload = {
            "api_version": "1",
            "auth": self.auth,
            "data": {
                "input": input,
                "method": method,
                "client": self.client_info
            }
        }

        retry_keywords = (
            'timeout',
            'connection',
            'bad gateway',
            'server error',
            '502',
            '503',
            '504'
        )

        for attempt in range(1, self.max_retries + 1):
            try:
                async with aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(ssl=False),
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as session:
                    async with session.post(self.base_url, json=payload) as res:
                        res.raise_for_status()
                        result = await res.json()
                        data = result.get("data") if isinstance(result, dict) else None

                        if not isinstance(data, dict):
                            return None

                        if data.get("status") == "OK":
                            output = data.get("output", data)

                            if getattr(self, 'as_dict', False):
                                return output

                            return Data(output)

                        status_detail = data.get("status_det")
                        exceptions.raise_exception(status_detail)

            except asyncio.TimeoutError as e:
                if attempt >= self.max_retries:
                    message = f"Request timed out after {self.max_retries}"
                    raise exceptions.TimeoutError(message) from None
                self.logger.warning(f"Request failed (attempt {attempt}/{self.max_retries}): Timeout")
                await asyncio.sleep(2 ** (attempt - 1))

            except aiohttp.ClientResponseError as e:
                if e.status in (500, 502, 503, 504):
                    if attempt >= self.max_retries:
                        raise exceptions.NoConnection() from None
                    self.logger.warning(f"Request failed (attempt {attempt}/{self.max_retries}): {e}")
                    await asyncio.sleep(2 ** (attempt - 1))
                else:
                    raise

            except aiohttp.ClientConnectionError as e:
                if attempt >= self.max_retries:
                    raise exceptions.NoConnection() from None
                self.logger.warning(f"Request failed (attempt {attempt}/{self.max_retries}): {e}")
                await asyncio.sleep(2 ** (attempt - 1))

            except Exception as e:
                error_msg = str(e).lower()

                if any(k in error_msg for k in retry_keywords):
                    if attempt >= self.max_retries:
                        raise exceptions.NoConnection() from None
                    self.logger.warning(f"Request failed (attempt {attempt}/{self.max_retries}): {e}")
                    await asyncio.sleep(2 ** (attempt - 1))
                else:
                    raise

        return None