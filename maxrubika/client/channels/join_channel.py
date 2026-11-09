from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class JoinChannel:
    async def join_channel(self: "maxrubika.Messenger", channel: str):
        """
        Join a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.

        Returns:
            Result of the API call.
        """
        from ..exceptions import InvalidInput

        chat_guid = await self.get_guid(channel)

        if not chat_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        if channel.startswith("https://rubika.ir/joinc"):
            link = channel.split('/')[-1]
            result = await self.request(
                method='joinChannelByLink',
                input={'hash_link': link}
            )
        else:
            input_data = {'channel_guid': chat_guid, 'action': 'Join'}
            result = await self.request(
                method='joinChannelAction',
                input=input_data
            )

        return result