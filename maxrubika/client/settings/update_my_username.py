import maxrubika
import re

class UpdateMyUsername:
    """
    Provides a method to update the username of the user.

    Methods:
        update_my_username: Update the username of the user.

    Attributes:
        self (maxrubika.Client): The maxrubika client instance.
    """
    async def update_my_username(
            self: "maxrubika.Client",
            username: str
    ) -> "maxrubika.types.Update":
        """
        Update the username of the user.

        Parameters:
            username (str): The new username for the user.
                - Must be between 7 and 32 characters
                - Can only contain English letters (a-z, A-Z), numbers (0-9), and underscore (_)
                - Should not start with number or underscore
                - Should not end with underscore

        Returns:
            maxrubika.types.Update: The updated user information after the username update.

        Raises:
            ValueError: If username doesn't meet the requirements.
        """
        username = username.replace('@', '').strip()

        if len(username) < 7:
            raise ValueError('Username must be at least 7 characters long.')
        if len(username) > 32:
            raise ValueError('Username must be at most 32 characters long.')

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError('Username can only contain English letters, numbers, and underscore (_).')

        if username[0].isdigit() or username.startswith('_'):
            raise ValueError('Username cannot start with a number or underscore.')

        if username.endswith('_'):
            raise ValueError('Username cannot end with underscore.')

        if not re.search(r'[a-zA-Z]', username):
            raise ValueError('Username must contain at least one letter.')
        
        return await self.request(name = 'updateUsername', input = {'username': username})