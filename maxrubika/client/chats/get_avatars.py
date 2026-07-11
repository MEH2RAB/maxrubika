import maxrubika
from ..exceptions import InvalidInput

class GetAvatars:
    async def get_avatars(self: "maxrubika.Client", chat: str):
        """
        Get avatars of a specific chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat to retrieve avatars for.

        Returns:
            The result of the API call.
        """
        if chat.lower() in ('me', 'cloud', 'self', 'myself'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")) and chat_guid != self.guid:
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        return await self.request(method = 'getAvatars', input = {'object_guid': chat_guid})