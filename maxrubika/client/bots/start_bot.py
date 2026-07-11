import maxrubika
from ..exceptions import InvalidInput

class StartBot:
    async def start_bot(self: "maxrubika.Client", bot: str):
        """
        Parameters:
            bot (str): The GUID or username of the bot.

        Returns:
            The result of the API call.
        """
        bot_guid = await self.get_guid(bot)

        if not bot_guid.startswith("b0"):
            message = f"'{bot}' does not point to a valid bot. Expected a bot GUID or bot username."
            raise InvalidInput(message)

        return await self.send_message(bot_guid, '/start')