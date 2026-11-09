from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UnpinChat:
    async def unpin_chat(self: "maxrubika.Messenger", chat: str):
        """
        Unpin a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat to unpin.

        Returns:
            Result of the operation.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {'object_guid': chat_guid, 'action': 'Unpin'}

        return await self.request(method='setActionChat', input=input_data)