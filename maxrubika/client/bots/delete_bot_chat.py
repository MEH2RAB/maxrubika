import maxrubika
from ..exceptions import InvalidInput

class DeleteBotChat:
    async def delete_bot_chat(
        self: "maxrubika.Client",
        bot: str
    ):
        """
        Delete a bot chat.

        Parameters:
            bot (str): The GUID or username of the bot.

        Returns:
            The result of the API call.
        """
        bot_guid = await self.get_guid(bot)

        if not bot_guid.startswith("b0"):
            message = f"'{bot}' does not point to a valid bot. Expected a bot GUID or bot username."
            raise InvalidInput(message)

        last_message = await self.get_last_message(bot_guid)
        last_data = last_message.to_dict() if hasattr(last_message, 'to_dict') else last_message

        message = last_data.get('message')

        if isinstance(message, dict):
            last_deleted_message_id = message.get('message_id', 0)
        else:
            last_deleted_message_id = 0

        return await self.request(
            method = 'deleteBotChat',
            input = {
                'bot_guid': bot_guid,
                'last_deleted_message_id': last_deleted_message_id
            }
        )