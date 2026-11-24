from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetUserInfo:
    async def get_user_info(self: "maxrubika.Bot", chat_id: str):
        """
        Get information about a user.

        Parameters:
            chat_id (str): chat_id of user. Must start with 'b0'.

        Returns:
            The API response with user information.
        """
        from .exceptions import InvalidInput

        if not chat_id.startswith("b0"):
            raise InvalidInput("'chat_id' must start with 'b0'.")

        return await self.get_chat_info(chat_id)