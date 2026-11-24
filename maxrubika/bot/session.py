import asyncio
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import aiohttp
    import maxrubika

logger = logging.getLogger(__name__)

class Session:
    async def _get_session(self: "maxrubika.Bot") -> "aiohttp.ClientSession":
        import aiohttp

        loop = asyncio.get_running_loop()

        if self._session is not None and not self._session.closed:
            if self._session_loop is loop:
                return self._session
            if not self._session_loop.is_closed():
                raise RuntimeError("The HTTP session belongs to a different event loop.")
 
            self._forget_session()

        timeout = aiohttp.ClientTimeout(total=self.timeout)
        connector = aiohttp.TCPConnector(ssl=False, limit=20)

        self._session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        self._session_loop = loop
        return self._session

    def _forget_session(self: "maxrubika.Bot") -> None:
        self._session = None
        self._session_loop = None

    async def close(self: "maxrubika.Bot") -> None:
        """Close the HTTP session. Must run in the loop that created it."""
        session = self._session
        if session is None:
            return

        if self._session_loop is not asyncio.get_running_loop():
            raise RuntimeError("close() must be awaited in the session's own event loop.")

        self._forget_session()

        try:
            if not session.closed:
                await session.close()
        except Exception:
            logger.debug("Error while closing session.", exc_info=True)

    def disconnect(self: "maxrubika.Bot") -> None:
        """Synchronous close. Don't call it from inside a running loop."""
        if self._session is None:
            return

        try:
            asyncio.get_running_loop()
        except RuntimeError:
            pass
        else:
            logger.warning("disconnect() called inside a running event loop. Use `await close()`.")
            return

        owner = self._session_loop

        if owner is None or owner.is_closed():
            logger.warning("Session's event loop is closed; dropping the session without a clean close.")
            self._forget_session()
            return

        try:
            if owner.is_running():
                asyncio.run_coroutine_threadsafe(self.close(), owner).result(timeout=10)
            else:
                owner.run_until_complete(self.close())
        except Exception:
            logger.debug("Error while closing session.", exc_info=True)
            self._forget_session()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()