import maxrubika
from ...data import Data

class GetFirstMessages:
    async def get_first_messages(
        self: "maxrubika.Client",
        chat: str,
        limit: int = 100
    ):
        """
        Get the first messages of a chat up to a limit.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            limit (int): Maximum number of messages to retrieve (max 100, min 1).

        Returns:
            List of first messages and count.
        """
        limit = max(1, min(limit, 100))
        chat_guid = await self.get_guid(chat)

        mid = "0"
        all_messages = []
        message_ids = set()

        while len(all_messages) < limit:
            result = await self.get_messages_interval(chat_guid, mid)
            data = result.to_dict() if hasattr(result, 'to_dict') else result
            messages = data.get('messages', [])

            if not messages:
                break

            for msg in messages:
                msg_id = int(msg.get('message_id') if isinstance(msg, dict) else msg.message_id)
                if msg_id not in message_ids:
                    message_ids.add(msg_id)
                    all_messages.append(msg.to_dict() if hasattr(msg, 'to_dict') else msg)
                    if len(all_messages) >= limit:
                        break

            new_min_id = data.get('new_min_id')
            if not new_min_id or str(new_min_id) == mid:
                break
            mid = str(new_min_id)

            if not data.get('new_has_continue', False):
                break

        return Data({
            "messages": all_messages[:limit],
            "count": len(all_messages[:limit])
        })