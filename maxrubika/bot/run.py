import asyncio
from typing import Optional, Union
import maxrubika

class Run:
    def run(
        self: "maxrubika.Bot",
        poll_interval: float = 0.005,
        webhook_url: Optional[str] = None,
        webhook_path: str = "/wk",
        host: str = "0.0.0.0",
        port: int = 8080,
    ) -> Union[None, "asyncio.Future"]:
        """
        Start the bot.

        Parameters:
            poll_interval (float): Seconds between polls in polling mode. Defaults to 0.005 seconds.
            webhook_url (str, optional): Public URL for webhook mode. Defaults to None.
            webhook_path (str): Path for the webhook receiver. Defaults to "/wk".
            host (str): Bind address for the webhook server. Defaults to "0.0.0.0".
            port (int): Bind port for the webhook server. Defaults to 8080.
        """
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            try:
                asyncio.run(self.start(
                    poll_interval=poll_interval,
                    webhook_url=webhook_url,
                    webhook_path=webhook_path,
                    host=host,
                    port=port,
                ))
            except KeyboardInterrupt:
                print("Bot stopped.")
            return None

        return self.start(
            poll_interval=poll_interval,
            webhook_url=webhook_url,
            webhook_path=webhook_path,
            host=host,
            port=port,
        )