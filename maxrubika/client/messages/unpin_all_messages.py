import maxrubika
from ...data import Data

class UnpinAllMessages:
    async def unpin_all_messages(self: "maxrubika.Client", chat: str):
        """
        Unpin all pinned messages in a group, channel, or private chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            Result containing unpinned count.
        """
        chat_guid = await self.get_guid(chat)

        pinned_result = await self.get_pinned_messages(chat_guid)
        pinned_data = pinned_result.to_dict() if hasattr(pinned_result, 'to_dict') else pinned_result

        pinned_ids = pinned_data.get('pinned_ids', [])

        if not pinned_ids:
            return Data({"status": "OK", "message": "No pinned messages to unpin."})

        for message_id in pinned_ids:
            await self.unpin_message(chat_guid, message_id)

        return Data({"status": "OK", "unpinned_count": len(pinned_ids)})