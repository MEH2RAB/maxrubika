import asyncio
import logging
import aiohttp
import maxrubika

logger = logging.getLogger(__name__)

class Session:
    async def _get_session(self: "maxrubika.Bot") -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            connector = aiohttp.TCPConnector(ssl=False, limit=20)
            self._session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
            )
            self._session_loop = asyncio.get_running_loop()
        return self._session

    def _forget_session(self: "maxrubika.Bot") -> None:
        self._session = None
        self._session_loop = None
        self._close_task = None

    async def close(self: "maxrubika.Bot") -> None:
        """Async close — must be awaited inside the session's loop."""
        session = self._session
        if session is not None and not session.closed:
            try:
                await session.close()
            except Exception:
                logger.debug("Error while closing session.", exc_info=True)
        self._forget_session()

    def _schedule_close(self: "maxrubika.Bot", loop: asyncio.AbstractEventLoop) -> None:
 
        future = asyncio.run_coroutine_threadsafe(self.close(), loop)
        self._close_task = future

    def disconnect(self: "maxrubika.Bot") -> None:
        """
        Close the session synchronously, from any context:
          - if a loop is running, schedule the close on it;
          - if the owning loop is running in another thread, schedule there;
          - otherwise, run a new/owner loop to completion.
        """
        session = self._session
        if session is None or session.closed:
            self._forget_session()
            return

        owner = self._session_loop

        try:
            current = asyncio.get_running_loop()
        except RuntimeError:
            current = None

        if current is not None:
            if owner is None or owner is current:
                self._close_task = current.create_task(self.close())
            elif owner.is_running():
                asyncio.run_coroutine_threadsafe(self.close(), owner)
            else:
                self._forget_session()
            return

        if owner is None:
            try:
                asyncio.run(self.close())
            except Exception:
                logger.debug("Error while closing session.", exc_info=True)
                self._forget_session()
        elif owner.is_closed():
            self._forget_session()
        elif owner.is_running():
            asyncio.run_coroutine_threadsafe(self.close(), owner)
        else:
            try:
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