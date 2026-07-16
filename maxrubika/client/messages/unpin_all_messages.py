import maxrubika
from ...data import Data

class UnpinAllMessages:
    async def unpin_all_messages(self: "maxrubika.Client", chat: str):
        """
        Unpin all pinned messages in a group, channel, or private chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            The update indicating the success of the operation.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'setPinMessage',
            input = {
                'object_guid': chat_guid,
                'action': 'UnpinAllMessages'
                }
            )