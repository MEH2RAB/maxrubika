import asyncio
import logging
import secrets
import time
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

logger = logging.getLogger(__name__)

_ENDPOINT_TYPES = (
    "ReceiveUpdate",
    "ReceiveInlineMessage",
    "ReceiveQuery",
    "GetSelectionItem",
    "SearchSelectionItems",
)

_SUBPATHS = (
    "",
    "/receiveUpdate",
    "/receiveInlineMessage",
    "/receiveQuery",
    "/getSelectionItem",
    "/searchSelectionItems",
)

class Start:
    async def _clear_old_updates(self) -> Optional[str]:
        return f"{int(time.time()):08x}" + secrets.token_hex(8)

    async def _poll_loop(self: "maxrubika.Bot", interval: float = 0.05) -> None:
        last_offset = await self._clear_old_updates()

        while True:
            try:
                updates = await self.get_updates(offset_id=last_offset, limit=100)

                if updates:
                    data = updates.to_dict() if hasattr(updates, "to_dict") else updates
                    inner = data.get("data", data) if isinstance(data, dict) else {}
                    if not isinstance(inner, dict):
                        inner = {}

                    if "next_offset_id" in inner:
                        last_offset = inner["next_offset_id"]

                    for raw_update in inner.get("updates") or []:
                        try:
                            event = self._parse_raw_update(raw_update)
                            await self._registry.feed(event)
                        except Exception:
                            logger.warning("Failed to process update.", exc_info=True)

            except asyncio.CancelledError:
                raise
            except Exception:
                logger.error("Poll loop error.", exc_info=True)
                await asyncio.sleep(1)

            await asyncio.sleep(interval)

    async def _start_webhook(
        self: "maxrubika.Bot",
        console,
        webhook_url: str,
        webhook_path: str,
        host: str,
        port: int,
    ):
        from aiohttp import web

        base = webhook_path.rstrip("/")

        app = web.Application()
        for sub in _SUBPATHS:
            app.router.add_post(f"{base}{sub}", self._handle_webhook)

        full_url = f"{webhook_url.rstrip('/')}{base}"

        for endpoint_type in _ENDPOINT_TYPES:
            try:
                await self.update_bot_endpoints(full_url, endpoint_type)
                console.print(f"Webhook registered: {endpoint_type} → {full_url}", style="cyan")
            except Exception as e:
                console.print(f"Failed to register {endpoint_type}: {e}", style="red")

        runner = web.AppRunner(app)
        await runner.setup()
        try:
            await web.TCPSite(runner, host, port).start()
        except BaseException:
            await runner.cleanup()
            raise

        console.print(f"Webhook server running on http://{host}:{port}{base}", style="cyan")
        return runner

    async def start(
        self: "maxrubika.Bot",
        poll_interval: float = 0.05,
        webhook_url: Optional[str] = None,
        webhook_path: str = "/wk",
        host: str = "0.0.0.0",
        port: int = 8080
    ) -> None:
        """
        Starts the bot, either by polling for updates or by running a webhook server.

        If a `webhook_url` is provided, sets up an aiohttp web server to receive real-time updates from the Rubika API. Otherwise, falls back to a long-polling mechanism to fetch updates continuously.

        Parameters:
            poll_interval (float): The interval (in seconds) between each polling operation when running in polling mode. Defaults to 0.05 seconds.
            webhook_url (str, optional): The base URL where the webhook server is accessible. If provided, the bot operates in webhook mode. Defaults to None.
            webhook_path (str): The URL path on the server to handle incoming webhook requests. Defaults to "/wk".
            host (str): The hostname or IP address to bind the webhook server. Use "0.0.0.0" to listen on all available interfaces. Defaults to "0.0.0.0".
            port (int): The port number on which the webhook server will listen. Defaults to 8080.

        Returns:
            None
        """
        from rich.console import Console

        console = Console(highlight=False)
        runner = None

        try:
            await self._registry.fire_startup()

            if webhook_url:
                runner = await self._start_webhook(console, webhook_url, webhook_path, host, port)
                await asyncio.Event().wait()
            else:
                console.print("Bot started in polling mode...\n", style="cyan")
                await self._poll_loop(poll_interval)

        finally:
            if runner is not None:
                try:
                    await runner.cleanup()
                except Exception:
                    logger.warning("Error while stopping webhook server.", exc_info=True)

            try:
                await self._registry.fire_shutdown()
            except Exception:
                logger.warning("Error during shutdown handlers.", exc_info=True)

            try:
                await self.close()
            except Exception:
                logger.warning("Error during close.", exc_info=True)