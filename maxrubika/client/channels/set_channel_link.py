import maxrubika
from ..exceptions import InvalidInput

class SetChannelLink:
    async def set_channel_link(self: "maxrubika.Client", channel: str):
        """
        Set a custom link for the channel.

        Parameters:
            channel (str): The GUID of the channel.

        Returns:
            The result of the API call.
        """
        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        return await self.request(method = 'setChannelLink', input = {'channel_guid': channel_guid})