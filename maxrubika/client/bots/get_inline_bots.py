from typing import Union, List
import maxrubika
from ..exceptions import InvalidInput

class GetInlineBots:
    async def get_inline_bots(
        self: "maxrubika.Client",
        bots: Union[str, List[str]]
    ):
        """
        Retrieve information about inline bots by their GUIDs or usernames.

        Parameters:
            bots (Union[str, List[str]]): A single bot GUID/username or a list of bot GUIDs/usernames.

        Returns:
            The result of the API call.
        """
        if isinstance(bots, str):
            bots = [bots]

        bot_guids = []
        for bot in bots:
            guid = await self.get_guid(bot)

            if not guid.startswith("b0"):
                raise InvalidInput(
                    f"'{bot}' does not point to a valid bot. Expected a bot GUID or username.")

            bot_guids.append(guid)

        return await self.request(
            method = 'getInlineBots',
            input = {'bot_guids': bot_guids}
        )