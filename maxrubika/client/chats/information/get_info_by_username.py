import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetInfoByUsername:
    async def get_info_by_username(
        self: "maxrubika.Messenger",
        username: str
    ):
        """
        Get a chat (user, bot, or channel) by its username.

        Parameters:
            username (str): The username of the chat.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidUsername

        username = username.replace('@', '')

        if len(username) < 3:
            raise InvalidUsername('Username must be at least 3 characters long.')

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

        return await self.request(method='getObjectByUsername', input={'username': username})