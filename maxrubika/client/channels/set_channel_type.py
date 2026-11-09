from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetChannelType:
    async def set_channel_type(
        self: "maxrubika.Messenger",
        channel: str,
        channel_type: Literal['Public', 'Private']
    ):
        """
        Set type of a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.
            channel_type (str): The new type of the channel. 'Public' or 'Private'.

        Returns:
            The result of the API call.
        """
        return await self.edit_channel_info(channel=channel, channel_type=channel_type)