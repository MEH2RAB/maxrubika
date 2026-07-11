from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class SeenChannelMessages:
    async def seen_channel_messages(
        self: "maxrubika.Client",
        channel: str,
        min_id: Union[int, str],
        max_id: Union[int, str]
    ):
        """
        Mark channel messages as seen within a specific range.

        Parameters:
            channel (str): The GUID, link, or username of the channel.
            min_id (Union[int, str]): The minimum message ID to mark as seen.
            max_id (Union[int, str]): The maximum message ID to mark as seen.

        Returns:
            The result of the API call.
        """
        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        return await self.request(
            method = 'seenChannelMessages',
            input = {
                'channel_guid': channel_guid,
                'min_id': min_id,
                'max_id': max_id
            }
        )