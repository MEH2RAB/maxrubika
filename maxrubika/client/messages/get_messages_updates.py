from time import time
import maxrubika

class GetMessagesUpdates:
    async def get_messages_updates(
        self: "maxrubika.Client",
        chat: str,
        state: int = round(time()) - 150
    ):
        """
        Get message updates for a specific chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat for which updates are requested.
            state (int): The state at which updates are requested. Defaults to a timestamp approximately 150 seconds ago.

        Returns:
            The message updates for the specified chat.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'getMessagesUpdates',
            input = {
                'object_guid': chat_guid,
                'state': state
            }
        )