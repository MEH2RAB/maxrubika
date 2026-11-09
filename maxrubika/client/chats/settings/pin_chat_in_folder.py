from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class PinChatInFolder:
    async def pin_chat_in_folder(
        self: "maxrubika.Messenger",
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

        input_data = {
            'action': 'Pin',
            'folder_id': folder_id,
            'object_guid': chat_guid
        }

        return await self.request(method='setPinChatInFolder', input=input_data)