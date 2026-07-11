import re; import maxrubika
from ..exceptions import InvalidUsername

class UpdateChannelUsername:
    async def update_channel_username(
        self: "maxrubika.Client",
        channel: str,
        username: str
    ):
        """
        Update the username of a channel.

        Parameters:
            channel (str): The GUID or username of the channel.
            username (str): The new username for the channel.
                Must be between 7 and 32 characters
                Can only contain English letters (a-z, A-Z), numbers (0-9), and underscore (_)
                Should not start with number or underscore
                Should not end with underscore

        Returns:
            The result of the API call.
        """
        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidUsername(message)

        username = username.replace('@', '').strip()

        if username == "":
            return await self.request(
                method = 'updateChannelUsername', 
                input = {'channel_guid': channel_guid, 'username': username}
            )

        if len(username) < 7:
            raise InvalidUsername('Username must be at least 7 characters long.')

        if len(username) > 32:
            raise InvalidUsername('Username must be at most 32 characters long.')

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise InvalidUsername('Username can only contain English letters, numbers, and underscore (_).')

        if username[0].isdigit() or username.startswith('_'):
            raise InvalidUsername('Username cannot start with a number or underscore.')

        if username.endswith('_'):
            raise InvalidUsername('Username cannot end with underscore.')

        if not re.search(r'[a-zA-Z]', username):
            raise InvalidUsername('Username must contain at least one letter.')

        return await self.request(
            method = 'updateChannelUsername', input = {'channel_guid': channel_guid, 'username': username}
        )