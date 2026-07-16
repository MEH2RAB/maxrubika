import asyncio
import aiohttp
import logging
import maxrubika
from ..core.cipher import Cipher

class GetUpdates:
    async def get_updates(self: "maxrubika.Client"):
        """
        Listen for updates from Rubika's WebSocket.

        Returns:
            None
        """
        asyncio.create_task(self._keep_socket())

        while True:
            try:
                async with self.connection.session.ws_connect(
                    self.connection.wss_url, proxy=self.proxy
                ) as ws:
                    self.connection.ws = ws

                    await ws.send_json({
                        "method": "handShake",
                        "auth": self.auth,
                        "api_version": "6",
                        "data": "",
                    })

                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            asyncio.create_task(self._handle_text_message(msg.json()))
                        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            self.logger.warning("WebSocket connection lost; initiating reconnect...")
                            break

            except (aiohttp.ServerTimeoutError, TimeoutError, aiohttp.ClientError) as e:
                self.logger.warning(f"WebSocket connection lost: {e}. Attempting reconnection in 3 seconds...")
                await asyncio.sleep(3)

    async def _keep_socket(self: "maxrubika.Client") -> None:

        while True:
            if self.connection.session.closed:
                break

            try:
                await asyncio.sleep(10)

                if self.connection.ws and not self.connection.ws.closed:
                    await self.connection.ws.send_json({})
                    await self.get_chats_updates()
                else:
                    self.logger.warning("WebSocket disconnected or already closed.")
            except Exception as e:
                self.logger.warning(f"WebSocket keep-alive failed: {e}", exc_info=True)

    async def _handle_text_message(self: "maxrubika.Client", msg_data: dict) -> None:

        data_enc = msg_data.get("data_enc") or msg_data.get("messenger")
        if not data_enc:
            self.logger.debug("Missing update data in message", extra={"data": msg_data})
            return

        if isinstance(data_enc, dict):
            try:
                user_guid = msg_data.get("user_guid")
                tasks = [
                    self.connection.handle_update(
                        name, {**update, "client": self, "user_guid": user_guid}
                    )
                    for name, updates in data_enc.items()
                    if isinstance(updates, list)
                    for update in updates
                ]
                await asyncio.gather(*tasks)
            except Exception as e:
                self.logger.error(f"Channel update error: {e}", extra={"data": msg_data})
            return

        try:
            decrypted_data = Cipher.decrypt(data_enc, key=self.key)
            user_guid = decrypted_data.pop("user_guid")

            tasks = [
                self.connection.handle_update(
                    name, {**update, "client": self, "user_guid": user_guid}
                )
                for name, updates in decrypted_data.items()
                if isinstance(updates, list)
                for update in updates
            ]

            await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error(
                f"Failed to handle WebSocket message: {e}",
                extra={"data": msg_data}
            )