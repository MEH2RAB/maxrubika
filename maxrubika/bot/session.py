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
            if self._session_loop is not loop:
                raise RuntimeError("The HTTP session belongs to a different event loop.")
            return self._session

        timeout = aiohttp.ClientTimeout(total=self.timeout)
        connector = aiohttp.TCPConnector(ssl=False, limit=20)

        self._session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        self._session_loop = loop
        return self._session

    def _forget_session(self: "maxrubika.Bot") -> None:
        self._session = None
        self._session_loop = None
        self._close_task = None

    async def close(self: "maxrubika.Bot") -> None:
        """Close the HTTP session gracefully in its owning event loop."""
        session = self._session

        if session is None:
            return

        try:
            if not session.closed:
                await session.close()
                await asyncio.sleep(0)
        except Exception:
            logger.debug("Error while closing session.", exc_info=True)
        finally:
            if self._session is session:
                self._forget_session()

    async def _close_and_wait(self: "maxrubika.Bot") -> None:
        task = self._close_task

        if task is None or task.done():
            task = asyncio.create_task(self.close())
            self._close_task = task

        try:
            await task
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.debug("Error while waiting for session close.", exc_info=True)

    def _run_close_blocking(self: "maxrubika.Bot", loop: asyncio.AbstractEventLoop) -> None:
        if loop.is_closed():
            logger.warning("Cannot close the HTTP session because its event loop is closed.")
            self._forget_session()
            return

        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self.close(), loop)
            self._close_task = future
            try:
                future.result(timeout=10)
            except Exception:
                logger.debug("Error while waiting for session close.", exc_info=True)
        else:
            try:
                loop.run_until_complete(self.close())
            except Exception:
                logger.debug("Error while closing session.", exc_info=True)
                self._forget_session()

    def disconnect(self: "maxrubika.Bot") -> None:
        """Synchronous close."""
        session = self._session

        if session is None:
            return

        if session.closed:
            self._forget_session()
            return

        owner = self._session_loop

        try:
            current = asyncio.get_running_loop()
        except RuntimeError:
            current = None

        if current is not None:
            if owner is current:
                task = self._close_task
                if task is None or task.done():
                    task = current.create_task(self.close())
                    self._close_task = task

                if not task.done():
                    try:
                        current.run_until_complete(task)
                    except RuntimeError:
                        logger.debug(
                            "Could not block on close task from running loop; task scheduled for completion.",
                        )
                    except Exception:
                        logger.debug("Error while waiting for session close.", exc_info=True)
                return

            if owner is not None and owner.is_running():
                future = asyncio.run_coroutine_threadsafe(self.close(), owner)
                self._close_task = future
                try:
                    future.result(timeout=10)
                except Exception:
                    logger.debug("Error while waiting for session close.", exc_info=True)
                return

            logger.warning(
                "Cannot synchronously close the session from another running event loop. Use await close()."
            )
            return

        if owner is None:
            try:
                asyncio.run(self.close())
            except Exception:
                logger.debug("Error while closing session.", exc_info=True)
                self._forget_session()
            return

        self._run_close_blocking(owner)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._close_and_wait()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()