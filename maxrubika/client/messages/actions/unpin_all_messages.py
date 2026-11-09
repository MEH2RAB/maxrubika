from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UnpinAllMessages:
    async def unpin_all_messages(self: "maxrubika.Messenger", chat: str):
        """
        Unpin all pinned messages in a group, channel, or private chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {
            'object_guid': chat_guid,
            'action': 'UnpinAllMessages'
        }

        return await self.request(method='setPinMessage', input=input_data)