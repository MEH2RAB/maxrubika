from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetScheduledMessages:
    async def get_scheduled_messages(
        self: "maxrubika.Messenger",
        chat: str,
        start_id: Optional[str] = None
    ):
        """
        Get scheduled messages in a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            start_id (str, optional): The ID to start fetching from. Defaults to None.

        Returns:
            The result of the API call containing scheduled messages.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {'object_guid': chat_guid}

        if start_id:
            input_data['start_id'] = start_id

        return await self.request(method='getScheduledHistory', input=input_data)