from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class DeleteBotChat:
    async def delete_bot_chat(
        self: "maxrubika.Client",
        bot: str,
        last_deleted_message_id: Union[str, int]
    ):
        """
        Delete a bot chat.

        Parameters:
            bot (str): The GUID or username of the bot.
            last_deleted_message_id (Union[str, int]): The last deleted message ID.

        Returns:
            The result of the API call.
        """
        bot_guid = await self.get_guid(bot)

        if not bot_guid.startswith("b0"):
            message = f"'{bot}' does not point to a valid bot. Expected a bot GUID or bot username."
            raise InvalidInput(message)

        return await self.request(
            method = 'deleteBotChat',
            input = {
                'bot_guid': bot_guid,
                'last_deleted_message_id': last_deleted_message_id
            }
        )