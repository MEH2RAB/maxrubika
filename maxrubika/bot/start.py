import asyncio
import time
import secrets
import logging
from typing import Optional
from aiohttp import web
import maxrubika

from rich.console import Console

console = Console(highlight=False)
logger = logging.getLogger(__name__)

class Start:
    async def _clear_old_updates(self) -> Optional[str]:
        now_time = int(time.time())
        now_hex = hex(now_time)[2:].zfill(8)
        random_part = secrets.token_hex(8)

        current_offset = now_hex + random_part

        return current_offset

    async def _poll_loop(self, interval: float = 0.005) -> None:
        last_offset = await self._clear_old_updates()

        while True:
            try:
                updates = await self.get_updates(
                    offset_id=last_offset,
                    limit=100
                )

                if updates:
                    data = updates.to_dict() if hasattr(updates, 'to_dict') else updates
                    inner_data = data.get('data', data) if isinstance(data, dict) else {}
                    raw_updates = inner_data.get('updates', []) if isinstance(inner_data, dict) else []

                    if "next_offset_id" in inner_data:
                        last_offset = inner_data["next_offset_id"]

                    if raw_updates:
                        for raw_update in raw_updates:
                            try:
                                event = self._parse_raw_update(raw_update)
                                await self._registry.feed(event)
                            except Exception as e:
                                logger.warning(f"Failed to process update: {e}")

            except KeyboardInterrupt:
                break
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Poll loop error: {e}")
                await asyncio.sleep(1)

            await asyncio.sleep(interval)

    async def start(
        self: "maxrubika.Bot",
        poll_interval: float = 0.005,
        webhook_url: Optional[str] = None,
        webhook_path: str = "/wk",
        host: str = "0.0.0.0",
        port: int = 8080,
    ) -> None:
        """
        Starts the server or polling mechanism with specified configurations.

        Parameters:
            poll_interval: The interval (in seconds) between each polling operation. Default is 0.005 seconds.
            webhook_url: Optional URL for webhook integration. If provided, webhooks will be used.
            webhook_path: The URL path on the server to handle webhook requests. Default is "/wk".
            host: The hostname or IP address to bind the server. Default is "0.0.0.0" (all interfaces).
            port: The port number on which to run the server. Default is 8080.

        Returns:
            None
        """
        await self._registry.fire_startup()

        try:
            if webhook_url:
                app = web.Application()
                webhook_base = webhook_path.rstrip("/")

                app.router.add_post(f"{webhook_base}", self._handle_webhook)
                app.router.add_post(f"{webhook_base}/receiveUpdate", self._handle_webhook)
                app.router.add_post(f"{webhook_base}/receiveInlineMessage", self._handle_webhook)
                app.router.add_post(f"{webhook_base}/receiveQuery", self._handle_webhook)
                app.router.add_post(f"{webhook_base}/getSelectionItem", self._handle_webhook)
                app.router.add_post(f"{webhook_base}/searchSelectionItems", self._handle_webhook)

                full_url = f"{webhook_url.rstrip('/')}{webhook_base}"

                for endpoint_type in [
                    'ReceiveUpdate',
                    'ReceiveInlineMessage',
                    'ReceiveQuery',
                    'GetSelectionItem',
                    'SearchSelectionItems',
                ]:
                    try:
                        await self.update_bot_endpoints(full_url, endpoint_type)
                        console.print(
                            f"Webhook registered: {endpoint_type} → {full_url}",
                            style="cyan"
                        )
                    except Exception as e:
                        console.print(
                            f"Failed to register {endpoint_type}: {e}",
                            style="cyan"
                        )

                runner = web.AppRunner(app)
                await runner.setup()
                site = web.TCPSite(runner, host, port)
                await site.start()
                console.print(
                    f"Webhook server running on http://{host}:{port}{webhook_base}",
                    style="cyan"
                )

                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    pass
                finally:
                    await runner.cleanup()

            else:
                console.print("Bot started in polling mode...\n", style="cyan")
                try:
                    await self._poll_loop(poll_interval)
                except KeyboardInterrupt:
                    pass

        finally:
            await self.close()
            await self._registry.fire_shutdown()