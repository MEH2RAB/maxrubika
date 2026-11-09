from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class LeaveChannel:
    async def leave_channel(self: "maxrubika.Messenger", channel: str):
        """
        Leave a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        input_data = {'channel_guid': channel_guid, 'action': 'Leave'}

        return await self.request(
            method='joinChannelAction',
            input=input_data
        )