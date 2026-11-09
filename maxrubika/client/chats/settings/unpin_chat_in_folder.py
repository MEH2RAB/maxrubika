from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UnpinChatInFolder:
    async def unpin_chat_in_folder(
        self: "maxrubika.Messenger",
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

        input_data = {
            'action': 'Unpin',
            'folder_id': folder_id,
            'object_guid': chat_guid
        }

        return await self.request(method='setPinChatInFolder', input=input_data)