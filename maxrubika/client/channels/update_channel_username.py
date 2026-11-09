import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UpdateChannelUsername:
    async def update_channel_username(
        self: "maxrubika.Messenger",
        channel: str,
        username: str
    ):
        """
        Update the username of a channel.

        Parameters:
            channel (str): The GUID or username of the channel.
            username (str): The new username. 7-32 chars, letters/numbers/underscore, cannot start with number/underscore, cannot end with underscore.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidUsername

        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidUsername(message)

        username = username.replace('@', '').strip()

        input_data = {'channel_guid': channel_guid, 'username': username}

        if username == "":
            return await self.request(
                method='updateChannelUsername',
                input=input_data
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
            method='updateChannelUsername',
            input=input_data
        )