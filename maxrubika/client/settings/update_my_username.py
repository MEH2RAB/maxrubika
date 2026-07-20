import re; import maxrubika
from ..exceptions import InvalidInput

class UpdateMyUsername:
    async def update_my_username(
        self: "maxrubika.Client",
        username: str
    ):
        """
        Update the username of the user.

        Parameters:
            username (str): The new username for the user.
                - Must be between 7 and 32 characters
                - Can only contain English letters (a-z, A-Z), numbers (0-9), and underscore (_)
                - Should not start with number or underscore
                - Should not end with underscore

        Returns:
            The updated user information.
        """
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

        return await self.request(mrthod = 'updateUsername', input = {'username': username})