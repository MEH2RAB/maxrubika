from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetChannelInfo:
    async def get_channel_info(self: "maxrubika.Bot", chat_id: str):
        """
        Get information about a channel.

        Parameters:
            chat_id (str): chat_id or username of channel. Must start with 'c0' or '@'.

        Returns:
            The API response with channel information.
        """
        from .exceptions import InvalidInput

        if not (chat_id.startswith("c0") or chat_id.startswith("@")):
            raise InvalidInput("'chat_id' must start with 'c0' or '@'.")

        return await self.get_chat_info(chat_id)