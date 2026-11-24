import asyncio
import signal
from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class Run:
    def run(
        self: "maxrubika.Bot",
        poll_interval: float = 0.05,
        webhook_url: Optional[str] = None,
        webhook_path: str = "/wk",
        host: str = "0.0.0.0",
        port: int = 8080,
    ) -> Union[None, "asyncio.Future"]:
        """
        Start the bot.

        Outside an event loop this blocks until the bot stops (Ctrl+C / SIGTERM stop it
        gracefully). Inside a running loop it schedules the bot and returns the Future;
        keep a reference to it.

        Parameters:
            poll_interval (float): Seconds between polls in polling mode. Defaults to 0.05.
            webhook_url (str, optional): Public URL for webhook mode. Defaults to None.
            webhook_path (str): Path for the webhook receiver. Defaults to "/wk".
            host (str): Bind address for the webhook server. Defaults to "0.0.0.0".
            port (int): Bind port for the webhook server. Defaults to 8080.
        """
        kwargs = dict(
            poll_interval=poll_interval,
            webhook_url=webhook_url,
            webhook_path=webhook_path,
            host=host,
            port=port
        )

        try:
            asyncio.get_running_loop()
        except RuntimeError:
            pass
        else:
            return asyncio.ensure_future(self.start(**kwargs))

        async def main() -> None:
            loop = asyncio.get_running_loop()
            task = asyncio.current_task()
            for sig in (signal.SIGINT, signal.SIGTERM):
                try:
                    loop.add_signal_handler(sig, task.cancel)
                except (NotImplementedError, RuntimeError, ValueError):
                    pass
            try:
                await self.start(**kwargs)
            except asyncio.CancelledError:
                pass

        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            pass
        return None