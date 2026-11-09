from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPinnedMessages:
    async def get_pinned_messages(
        self: "maxrubika.Messenger",
        chat: str
    ):
        """
        Get all pinned messages from a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            Dictionary containing pinned messages and pinned IDs.
        """
        from ....data import Data

        chat_guid = await self.get_guid(chat)

        chat_info = await self.get_chat_info(chat_guid)

        if isinstance(chat_info, dict):
            chat_info = Data(chat_info)

        pinned_ids = chat_info.find_keys('pinned_message_ids')

        if not pinned_ids:
            no_pinned = {"status": "OK", "message": "No pinned messages."}
            if getattr(self, 'as_dict', False):
                return no_pinned
            return Data(no_pinned)

        messages_result = await self.get_messages_by_id(chat_guid, pinned_ids)

        if isinstance(messages_result, dict):
            messages_result = Data(messages_result)

        messages = messages_result.find_keys('messages') or []

        result_dict = {
            "messages": messages,
            "count": len(messages),
            "pinned_ids": pinned_ids
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)