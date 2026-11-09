from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class CheckUserUsername:
    async def check_user_username(self: "maxrubika.Messenger", username: str):
        """
        Check the availability of a username for a user.

        Parameters:
            username (str): The username to be checked.

        Returns:
            The result of the username availability check.
        """
        return await self.request(method='checkUserUsername', input={'username': username.replace('@', '')})