from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ArchiveChat:
    async def archive_chat(
        self: "maxrubika.Messenger",
        chat: str
    ):
        """
        Archive a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat to archive.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {'object_guid': chat_guid, 'action': 'Archive'}

        return await self.request(method='setActionChat', input=input_data)