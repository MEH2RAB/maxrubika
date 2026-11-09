from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UnmuteChat:
    async def unmute_chat(self: "maxrubika.Messenger", chat: str):
        """
        Unmute a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat to unmute.

        Returns:
            Result of the operation.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {'object_guid': chat_guid, 'action': 'Unmute'}

        return await self.request(method='setActionChat', input=input_data)