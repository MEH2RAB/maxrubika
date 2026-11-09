from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ClearChatDraft:
    async def clear_chat_draft(
        self: "maxrubika.Messenger",
        chat: str
    ):
        """
        Clear the draft of a specific chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {
            'action': 'Selected',
            'object_guid': chat_guid
        }

        return await self.request(method='clearDrafts', input=input_data)