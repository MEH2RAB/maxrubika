import maxrubika
from ..exceptions import InvalidInput

class JoinChannel:
    async def join_channel(self: "maxrubika.Client", channel: str):
        """
        Join a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.

        Returns:
            Result of the API call.
        """
        chat_guid = await self.get_guid(channel)

        if not chat_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        if channel.startswith("https://rubika.ir/joinc"):
            link = channel.split('/')[-1]
            result = await self.request(
                method = 'joinChannelByLink',
                input = {'hash_link': link}
            )
        else:
            result = await self.request(
                method = 'joinChannelAction',
                input = {'channel_guid': chat_guid, 'action': 'Join'}
            )

        return result