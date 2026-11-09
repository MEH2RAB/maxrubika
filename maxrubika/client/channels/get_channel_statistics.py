from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetChannelStatistics:
    async def get_channel_statistics(
        self: "maxrubika.Messenger",
        channel: str
    ):
        """
        Get all statistics for a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.

        Returns:
            The result of the API call containing channel statistics.
        """
        from ..exceptions import InvalidInput

        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        return await self.request(
            method='getAllStatistics',
            input={'channel_guid': channel_guid}
        )