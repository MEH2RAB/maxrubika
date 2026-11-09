from typing import Optional, Coroutine, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class Run:
    async def run(self: "maxrubika.Messenger", coroutine: Optional[Coroutine] = None):
        """
        Start the client and listen for updates.

        Parameters:
            coroutine (Coroutine, optional): Optional coroutine to run before listening for updates.

        Returns:
            None when used normally (runs forever until stopped).
        """
        if not getattr(self, 'connection', None):
            await self.start()
        if coroutine is not None:
            await coroutine
        return await self.get_updates()