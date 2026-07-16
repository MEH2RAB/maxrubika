import maxrubika
from ..exceptions import InvalidInput

class PinChatInFolder:
    async def pin_chat_in_folder(
        self: "maxrubika.Client",
        chat: str,
        folder_id: str
    ):
        """
        Pin a chat in a folder.

        Parameters:
            chat (str): The GUID, link, or username of the chat to pin.
            folder_id (str): The folder ID to pin the chat in.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'setPinChatInFolder',
            input = {
                'action': 'Pin',
                'folder_id': folder_id,
                'object_guid': chat_guid
            }
        )