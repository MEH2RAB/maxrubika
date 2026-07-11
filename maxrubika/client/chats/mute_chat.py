import maxrubika

class MuteChat:
    async def mute_chat(self: "maxrubika.Client", chat: str):
        """
        Mute a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat to mute.

        Returns:
            Result of the operation.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'setActionChat',
            input = {'object_guid': chat_guid, 'action': 'Mute'}
        )