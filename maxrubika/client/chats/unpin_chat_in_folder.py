import maxrubika
from ..exceptions import InvalidInput

class UnpinChatInFolder:
    async def unpin_chat_in_folder(
        self: "maxrubika.Client",
        chat: str,
        folder_id: str
    ):
        """
        Unpin a chat from a folder.

        Parameters:
            chat (str): The GUID, link, or username of the chat to unpin.
            folder_id (str): The folder ID to unpin the chat from.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'setPinChatInFolder',
            input = {
                'action': 'Unpin',
                'folder_id': folder_id,
                'object_guid': chat_guid
            }
        )