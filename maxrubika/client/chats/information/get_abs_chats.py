from typing import Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetAbsChats:
    async def get_abs_chats(
        self: "maxrubika.Messenger",
        chats: Union[str, List[str]]
    ):
        """
        Get abstract info (title, avatar, etc.) for multiple chats (users, bots, groups, channels).

        Parameters:
            chats (Union[str, List[str]]): A single chat (GUID, username, or link) or a list of them.

        Returns:
            The result of the API call, containing `abs_objects`.
        """
        if isinstance(chats, str):
            chats = [chats]

        chat_guids = []
        for chat in chats:
            guid = await self.get_guid(chat)
            chat_guids.append(guid)

        return await self.request(
            method='getAbsObjects',
            input={'objects_guids': chat_guids}
        )