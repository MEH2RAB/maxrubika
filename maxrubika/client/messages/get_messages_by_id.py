from typing import Union
import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class GetMessagesByID:
    async def get_messages_by_id(
        self: "maxrubika.Client",
        chat: str,
        message_ids: Union[str, int, list]
    ):
        """
        Retrieve messages by their IDs.

        Parameters:
            chat (str): The GUID, link, or username of the chat to which the messages belong.
            message_ids (Union[str, int, list]): The ID or list of IDs of the messages to retrieve.

        Returns:
            The retrieved messages identified by their IDs.
        """
        chat_guid = await self.get_guid(chat)

        if isinstance(message_ids, (str, int)):
            message_ids = [str(message_ids)]
        elif isinstance(message_ids, list):
            message_ids = [str(mid) for mid in message_ids]

        if not message_ids:
            raise InvalidInput("At least one message ID is required.")

        if len(message_ids) > 20:
            chunks = [
                message_ids[i:i + 20]
                for i in range(0, len(message_ids), 20)
            ]

            all_messages = []
            for chunk in chunks:
                result = await self.request(
                    method = 'getMessagesByID',
                    input = {
                        'object_guid': chat_guid,
                        'message_ids': chunk
                    }
                )
                result_data = result.to_dict() if hasattr(result, 'to_dict') else result
                all_messages.extend(result_data.get('messages', []))

            return Data({
                "status": "OK",
                "messages": all_messages,
                "count": len(all_messages)
            })

        result = await self.request(
            method = 'getMessagesByID',
            input = {
                'object_guid': chat_guid,
                'message_ids': message_ids
            }
        )

        return result