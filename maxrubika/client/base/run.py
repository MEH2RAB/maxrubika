from typing import Optional, Coroutine
import asyncio

class Run:
    async def run(self, coroutine: Optional[Coroutine] = None):
        """
        Start the client and listen for updates.

        Ensures the connection is established, then optionally runs a provided coroutine
        before entering the update loop. Works both in sync and async contexts.

        Parameters:
            coroutine: Optional coroutine to run before listening for updates.

        Returns:
            None when used normally (runs forever until stopped).

        Sync usage:
            app = Client("session")
            app.run()

        Async usage:
            async with Client("session") as app:
                await app.run()
        """
        if not getattr(self, 'connection', None):
            await self.start()
        if coroutine is not None:
            await coroutine
        return await self.get_updates()