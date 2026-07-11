import maxrubika
from ..exceptions import InvalidInput

class GetChannelInfo:
    async def get_channel_info(self: "maxrubika.Client", channel: str):
        """
        Get information about a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.

        Returns:
            The result of the API call.
        """
        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        return await self.request(method = 'getChannelInfo', input = {'channel_guid': channel_guid})