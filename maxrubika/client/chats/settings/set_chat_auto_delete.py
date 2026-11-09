from typing import Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetChatAutoDelete:
    async def set_chat_auto_delete(
        self: "maxrubika.Messenger",
        chat: Union[str, List[str]],
        auto_delete: Union[str, int]
    ):
        """
        Set auto-delete timer for one or more groups or channels.

        Parameters:
            chat (Union[str, List[str]]): The GUID, link, username of a group/channel, or a list of them.
            auto_delete (Union[str, int]): Auto-delete duration. Accepts: int (1-365 days), str ('1m'-'60m', '1h'-'24h', '1d'-'365d', '1w'-'52w', '1y', 'off'), or words ('day', 'week', 'month', 'year', 'never', 'disabled').

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        if isinstance(chat, str):
            chat = [chat]

        chat_guids = []

        for c in chat:
            guid = await self.get_guid(c)

            if not guid.startswith(("g0", "c0")):
                message = f"'{c}' does not point to a valid group or channel. Auto-delete can only be set for groups and channels."
                raise InvalidInput(message)

            chat_guids.append(guid)

        auto_delete_value = self._parse_auto_delete(auto_delete)

        input_data = {
            'object_guids': chat_guids,
            'auto_delete': auto_delete_value
        }

        return await self.request(method='setAutoDelete', input=input_data)