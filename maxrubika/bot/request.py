import json
import asyncio
import logging
from typing import Optional, Dict, Any, TYPE_CHECKING

from ..data import Data

if TYPE_CHECKING:
    import maxrubika

logger = logging.getLogger(__name__)

class Response(Data):
    pass

class Request:
    async def request(
        self: "maxrubika.Bot",
        method: str,
        input: Optional[Dict[str, Any]] = None
    ):
        """
        Send a request to the Bot API with automatic retry and error mapping.

        Parameters:
            method (str): The API method name, appended to `base_url`, e.g. "getMe".
            input (dict, optional): The request payload sent as JSON body.

        Returns:
            The parsed API response.
        """
        from .exceptions import (
            APIException, Network,
            Timeout, BadGateway,
            JSONDecode, ServerError,
            InvalidInput, InvalidAccess,
            TooRequests,
        )

        url = f"{self.base_url}/{method}"
        session = await self._get_session()
        last_error = None

        for attempt in range(self.max_retries):
            try:
                async with session.post(url, json=input or {}) as resp:
                    text = (await resp.text()).strip()

                    if resp.status == 502:
                        raise BadGateway(dev_message="Server returned 502")

                    if resp.status == 500:
                        raise ServerError(dev_message="Server returned error")

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
                            else:
                                raise APIException(status=api_status, dev_message=error_message)

                    if getattr(self, 'as_dict', False):
                        return data
                    return Response(data)

            except (BadGateway, ServerError, Timeout, asyncio.TimeoutError) as e:
                if isinstance(e, asyncio.TimeoutError):
                    e = Timeout(dev_message=f"Request timed out after {self.timeout}s")

                if attempt < self.max_retries - 1:
                    logger.warning(
                        f"Request failed - Attempt {attempt + 1}/{self.max_retries}: {type(e).__name__}"
                    )
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise e from None

            except (JSONDecode, InvalidInput, InvalidAccess, TooRequests, APIException):
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
        raise Network(
            dev_message=f"Failed to call {method} after {self.max_retries} attempts."
        )