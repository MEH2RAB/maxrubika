from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetAvatars:
    async def get_avatars(self: "maxrubika.Messenger", chat: str):
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

        return await self.request(method='getAvatars', input={'object_guid': chat_guid})