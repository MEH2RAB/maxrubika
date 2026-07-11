import maxrubika

class PinChat:
    async def pin_chat(self: "maxrubika.Client", chat: str):
        """
        Pin a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat to pin.

        Returns:
            Result of the operation.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'setActionChat',
            input = {'object_guid': chat_guid, 'action': 'Pin'}
        )