from typing import Optional, Union
from time import time
import maxrubika

class GetChatsUpdates:
    async def get_chats_updates(
        self: "maxrubika.Client",
        state: Optional[Union[str, int]] = None
    ):
        """
        Get updates for chats.

        Parameters:
            state (Optional[Union[str, int]]): State parameter for syncing updates. If not provided,
                it uses the current time minus 150 seconds.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'getChatsUpdates',
            input = {'state': round(time()) - 150 if state is None else int(state)}
        )