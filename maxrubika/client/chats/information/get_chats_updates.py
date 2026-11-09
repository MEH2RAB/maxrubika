from typing import Optional, Union, TYPE_CHECKING
from time import time

if TYPE_CHECKING:
    import maxrubika

class GetChatsUpdates:
    async def get_chats_updates(
        self: "maxrubika.Messenger",
        state: Optional[Union[str, int]] = None
    ):
        """
        Get updates for chats.

        Parameters:
            state (Union[str, int], optional): State parameter for syncing updates. If not provided, uses current time minus 150 seconds.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method='getChatsUpdates',
            input={'state': round(time()) - 150 if state is None else int(state)}
        )