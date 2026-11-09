from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetLastMessages:
    async def get_last_messages(
        self: "maxrubika.Messenger",
        chat: str,
        limit: int = 100
    ):
        """
        Get the last messages of a chat up to a limit.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            limit (int): Maximum number of messages to retrieve (max 500).

        Returns:
            List of last messages and count.
        """
        from ....data import Data

        chat_guid = await self.get_guid(chat)

        limit = max(1, min(limit, 500))

        max_id = None
        all_messages = []
        message_ids = set()

        while len(all_messages) < limit:
            input_data = {
                'object_guid': chat_guid,
                'sort': 'FromMax',
                'limit': 25
            }
            if max_id is not None:
                input_data['max_id'] = max_id

            result = await self.request(
                method='getMessages',
                input=input_data
            )

            if isinstance(result, dict):
                result = Data(result)

            messages = result.find_keys('messages') or []

            if not messages:
                break

            for msg in messages:
                msg_data = Data(msg) if isinstance(msg, dict) else msg
                msg_id = msg_data.find_keys('message_id')

                if not msg_id:
                    continue

                msg_id_int = int(msg_id)

                if msg_id_int not in message_ids:
                    message_ids.add(msg_id_int)
                    all_messages.append(msg_data.to_dict())

                    if len(all_messages) >= limit:
                        break

            if len(all_messages) >= limit:
                break

            new_max_id = result.find_keys('new_max_id')

            if not new_max_id or str(new_max_id) == max_id:
                break

            max_id = str(new_max_id)

        result_dict = {
            "messages": all_messages[:limit],
            "count": len(all_messages[:limit])
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)