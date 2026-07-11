from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class GetChannelSeenCount:
    async def get_channel_seen_count(
        self: "maxrubika.Client",
        channel: str,
        min_id: Union[str, int],
        max_id = Union[str, int]
    ):
        """
        Get the view count of a channel within a specific message ID range.

        Parameters:
            channel (str): The GUID, link, or username of the channel.
            min_id (Union[str, int]): Minimum message ID in the range (inclusive).
            max_id (Union[str, int]): Maximum message ID in the range (inclusive).

        Returns:
            The result of the API call.
        """
        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        return await self.request(
            method = 'getChannelSeenCount',
            input = {
                'channel_guid': channel_guid,
                'min_id': min_id,
                'max_id': max_id
            }
        )