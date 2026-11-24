from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetGroupInfo:
    async def get_group_info(self: "maxrubika.Bot", chat_id: str):
        """
        Get information about a group.

        Parameters:
            chat_id (str): chat_id of group. Must start with 'g0'.

        Returns:
            The API response with group information.
        """
        from .exceptions import InvalidInput

        if not chat_id.startswith("g0"):
            raise InvalidInput("'chat_id' must start with 'g0'.")

        return await self.get_chat_info(chat_id)