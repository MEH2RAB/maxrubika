from typing import Optional, Coroutine
import asyncio

class Run:
    async def run(self, coroutine: Optional[Coroutine] = None):
        """
        Start the client and listen for updates.

        Parameters:
            coroutine: Optional coroutine to run before listening for updates.

        Returns:
            None when used normally (runs forever until stopped).
        """
        if not getattr(self, 'connection', None):
            await self.start()
        if coroutine is not None:
            await coroutine
        return await self.get_updates()