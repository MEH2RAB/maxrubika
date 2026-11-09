from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SeenChannelMessages:
    async def seen_channel_messages(
        self: "maxrubika.Messenger",
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
        from ..exceptions import InvalidInput

        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        input_data = {
            'channel_guid': channel_guid,
            'min_id': min_id,
            'max_id': max_id
        }

        return await self.request(
            method='seenChannelMessages',
            input=input_data
        )