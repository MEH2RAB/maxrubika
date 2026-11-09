import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UpdateMyUsername:
    async def update_my_username(
        self: "maxrubika.Messenger",
        username: str
    ):
        """
        Update the username of the user.

        Parameters:
            username (str): The new username (7-32 chars, letters/numbers/underscore, cannot start with number/underscore, cannot end with underscore).

        Returns:
            The updated user information.
        """
        from ...exceptions import InvalidInput

        username = username.replace('@', '').strip()

        if len(username) < 7:
            raise InvalidInput('Username must be at least 7 characters long.')
        if len(username) > 32:
            raise InvalidInput('Username must be at most 32 characters long.')

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise InvalidInput('Username can only contain English letters, numbers, and underscore (_).')

        if username[0].isdigit() or username.startswith('_'):
            raise InvalidInput('Username cannot start with a number or underscore.')

        if username.endswith('_'):
            raise InvalidInput('Username cannot end with underscore.')

        if not re.search(r'[a-zA-Z]', username):
            raise InvalidInput('Username must contain at least one letter.')

        return await self.request(method='updateUsername', input={'username': username})