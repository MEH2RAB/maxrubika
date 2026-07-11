import maxrubika
from ...data import Data

class GetLastMessages:
    async def get_last_messages(
        self: "maxrubika.Client",
        chat: str,
        limit: int = 100
    ):
        """
        Get the last messages of a chat up to a limit.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            limit (int): Maximum number of messages to retrieve (max 100).

        Returns:
            List of last messages and count.
        """
        chat_guid = await self.get_guid(chat)

        limit = max(1, min(limit, 100))

        max_id = None
        all_messages = []
        message_ids = set()

        while len(all_messages) < limit:
            result = await self.request(
                method='getMessages',
                input={
                    'object_guid': chat_guid,
                    'sort': 'FromMax',
                    'max_id': max_id,
                    'limit': 25
                }
            )

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

            if len(all_messages) >= limit:
                break

            new_max_id = data.get('new_max_id')
            if not new_max_id or str(new_max_id) == max_id:
                break
            max_id = str(new_max_id)

        return Data({
            "messages": all_messages[:limit],
            "count": len(all_messages[:limit])
        })