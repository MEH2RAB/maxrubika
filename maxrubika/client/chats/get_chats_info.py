from typing import Union, List
import maxrubika
from ..exceptions import InvalidInput

class GetChatsInfo:
    async def get_chats_info(
        self: "maxrubika.Client",
        chats: Union[str, List[str]]
    ):
        """
        Get information about multiple chats by their GUIDs.

        Parameters:
            chats (Union[str, List[str]]): A single chat GUID or a list of chat GUIDs.

        Returns:
            The result of the API call containing chats information.
        """
        if isinstance(chats, str):
            chats = [chats]

        chat_guids = []
        for chat in chats:
            guid = await self.get_guid(chat)
            chat_guids.append(guid)

        return await self.request(
            method = 'getChatsByID',
            input = {'object_guids': chat_guids}
        )