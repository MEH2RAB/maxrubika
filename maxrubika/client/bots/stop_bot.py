from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class StopBot:
    async def stop_bot(self: "maxrubika.Messenger", bot: str):
        """
        Stop a bot.

        Parameters:
            bot (str): The GUID or username of the bot.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

        bot_guid = await self.get_guid(bot)

        if not bot_guid.startswith("b0"):
            message = f"'{bot}' does not point to a valid bot. Expected a bot GUID or bot username."
            raise InvalidInput(message)

        return await self.request(method='stopBot', input={'bot_guid': bot_guid})