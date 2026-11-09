from typing import Union, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class MarkAsSeen:
    async def mark_as_seen(
        self: "maxrubika.Messenger",
        chat: str,
        message_id: Optional[Union[str, int]] = None
    ):
        """
        Mark a specific message as seen.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int], optional): Specific message ID. Defaults to last message.

        Returns:
            Result of the operation.
        """
        from ....data import Data

        chat_guid = await self.get_guid(chat)

        if message_id is None:
            last_message = await self.get_last_message(chat_guid)

            if isinstance(last_message, dict):
                last_message = Data(last_message)

            message_id = last_message.find_keys('message_id')

            if message_id is None:
                no_msg = {"status": "OK", "message": "No messages found to mark as seen."}
                if getattr(self, 'as_dict', False):
                    return no_msg
                return Data(no_msg)

        return await self.seen_chats({chat_guid: str(message_id)})