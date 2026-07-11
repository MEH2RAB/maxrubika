import maxrubika
from ..exceptions import InvalidInput

class RemoveFromTopUsers:
    async def remove_from_top_users(self: "maxrubika.Client", user: str):
        """
        Remove user from top users list.

        Parameters:
            user (str): The user GUID or username to remove.

        Returns:
            The result of the API call.
        """
        user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        return await self.request(
            method = 'removeFromTopChatUsers',
            input = {'user_guid': user_guid}
        )