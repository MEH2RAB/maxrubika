import maxrubika
from ..exceptions import InvalidInput

class LeaveChannel:
    async def leave_channel(self: "maxrubika.Client", channel: str):
        """
        Leave a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.

        Returns:
            The result of the API call.
        """
        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        return await self.request(
            method = 'joinChannelAction',
            input = {'channel_guid': channel_guid, 'action': 'Leave'}
        )