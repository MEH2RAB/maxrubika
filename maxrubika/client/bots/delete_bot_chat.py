from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteBotChat:
    async def delete_bot_chat(
        self: "maxrubika.Messenger",
        bot: str
    ):
        """
        Delete a bot chat.

        Parameters:
            bot (str): The GUID or username of the bot.

        Returns:
            The result of the API call.
        """
        from ...data import Data
        from ..exceptions import InvalidInput

        bot_guid = await self.get_guid(bot)

        if not bot_guid.startswith("b0"):
            message = f"'{bot}' does not point to a valid bot. Expected a bot GUID or bot username."
            raise InvalidInput(message)

        last_message = await self.get_last_message(bot_guid)

        if isinstance(last_message, dict):
            last_message = Data(last_message)

        last_deleted_message_id = last_message.find_keys('message_id') or 0

        input_data = {
            'bot_guid': bot_guid,
            'last_deleted_message_id': last_deleted_message_id
        }

        return await self.request(
            method='deleteBotChat',
            input=input_data
        )