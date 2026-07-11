import maxrubika
from ..exceptions import InvalidInput

class JoinChat:
    async def join_chat(self: "maxrubika.Client", chat: str):
        """
        Join a chat (channel or group).

        Parameters:
            chat (str): The GUID, link, or username of the chat (channel or group).

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        if chat_guid.startswith('c0'):
            return await self.join_channel(chat)
        else:
            return await self.join_group(chat)