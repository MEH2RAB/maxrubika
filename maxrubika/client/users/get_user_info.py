import maxrubika
from ..exceptions import InvalidInput

class GetUserInfo:
    async def get_user_info(self: "maxrubika.Client", user: str = None):
        """
        Get information about a specific user.

        Parameters:
            user (str): The GUID or username of the user.

        Returns:
            Information about the specified user.
        """
        if user is None:
            user_guid = None
        else:
            user_guid = await self.get_guid(user)

            if not user_guid.startswith("u0"):
                message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
                raise InvalidInput(message)

        return await self.request(
            method = 'getUserInfo',
            input = {} if user_guid is None else {'user_guid': user_guid},
            tmp_session = True if self.auth is None else False
        )