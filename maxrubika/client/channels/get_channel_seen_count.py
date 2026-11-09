from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetChannelSeenCount:
    async def get_channel_seen_count(
        self: "maxrubika.Messenger",
        channel: str,
        min_id: Union[str, int],
        max_id: Union[str, int]
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
            method='getChannelSeenCount',
            input=input_data
        )