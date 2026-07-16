from typing import Union, List
import re
import maxrubika
from ..exceptions import InvalidInput

class SetChatAutoDelete:
    async def set_chat_auto_delete(
        self: "maxrubika.Client",
        chat: Union[str, List[str]],
        auto_delete: Union[str, int]
    ):
        """
        Set auto-delete timer for one or more groups or channels.

        Parameters:
            chat (Union[str, List[str]]): The GUID, link, username of a group/channel, or a list of them.
            auto_delete (Union[str, int]): Auto-delete duration. Accepts:
                - Integer: 1-365 (days)
                - String: '1m'-'60m', '1h'-'24h', '1d'-'365d', '1w'-'52w', '1y', 'off'
                - Common words: 'day', 'week', 'month', 'year', 'never', 'disabled'

        Returns:
            The result of the API call.
        """
        if isinstance(chat, str):
            chat = [chat]

        chat_guids = []
        for c in chat:
            guid = await self.get_guid(c)
            if not guid.startswith(("g0", "c0")):
                raise InvalidInput(
                    f"'{c}' does not point to a valid group or channel. "
                    "Auto-delete can only be set for groups and channels."
                )
            chat_guids.append(guid)

        auto_delete = self._parse_auto_delete(auto_delete)

        return await self.request(
            method = 'setAutoDelete',
            input = {
                'object_guids': chat_guids,
                'auto_delete': auto_delete
            }
        )