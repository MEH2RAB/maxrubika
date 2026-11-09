from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetFirstMessages:
    async def get_first_messages(
        self: "maxrubika.Messenger",
        chat: str,
        limit: int = 100
    ):
        """
        Get the first messages of a chat up to a limit.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            limit (int): Maximum number of messages to retrieve (max 500, min 1).

        Returns:
            List of first messages and count.
        """
        from ....data import Data

        limit = max(1, min(limit, 500))
        chat_guid = await self.get_guid(chat)

        mid = "0"
        all_messages = []
        message_ids = set()

        while len(all_messages) < limit:
            result = await self.get_messages_interval(chat_guid, mid)

            if isinstance(result, dict):
                result = Data(result)

            messages = result.find_keys('messages') or []

            if not messages:
                break

            for msg in messages:
                msg_id = msg.find_keys('message_id')
                if not msg_id:
                    continue

                msg_id_int = int(msg_id)

                if msg_id_int not in message_ids:
                    message_ids.add(msg_id_int)
                    all_messages.append(msg.to_dict())

                    if len(all_messages) >= limit:
                        break

            if len(all_messages) >= limit:
                break

            new_min_id = result.find_keys('new_min_id')

            if not new_min_id or str(new_min_id) == mid:
                break

            mid = str(new_min_id)

            new_has_continue = result.find_keys('new_has_continue')

            if not new_has_continue:
                break

        result_dict = {
            "messages": all_messages[:limit],
            "count": len(all_messages[:limit])
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)