import maxrubika

class ArchiveChat:
    async def archive_chat(
        self: "maxrubika.Client",
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

        return await self.request(
            method = 'setActionChat',
            input = {'object_guid': chat_guid, 'action': 'Archive'}
        )