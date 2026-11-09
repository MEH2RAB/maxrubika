from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class CheckChannelUsername:
    async def check_channel_username(self: "maxrubika.Messenger", username: str):
        """
        Check the availability of a username for a channel.

        Parameters:
            username (str): The username to check.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method='checkChannelUsername',
            input={'username': username.replace('@', '')}
        )