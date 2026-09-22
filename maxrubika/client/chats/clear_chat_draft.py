import maxrubika

class ClearChatDraft:
    async def clear_chat_draft(
        self: "maxrubika.Client",
        chat: str
    ):
        """
        Clear the draft of a specific chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'clearDrafts',
            input = {
                'action': 'Selected',
                'object_guid': chat_guid
            }
        )