from typing import Union, Literal
import maxrubika
from ..exceptions import InvalidInput

class DeleteMessages:
    async def delete_messages(
        self: "maxrubika.Client",
        chat: str,
        message_ids: Union[str, int, list],
        type: Literal['Local', 'Global', 'Scheduled'] = 'Global'
    ):
        """
        Delete specified messages associated with the given chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat associated with the messages
                (e.g., user, group, channel).
            message_ids (Union[str, int, list]): The ID or list of IDs of the messages to be deleted.
            type (str): The type of deletion, can be 'Global', 'Local', or 'Scheduled'. Default is 'Global'.

        Returns:
            The updated information after deleting the messages.
        """
        chat_guid = await self.get_guid(chat)

        if type not in ('Global', 'Local', 'Scheduled'):
            raise InvalidInput("'type' argument can only be in 'Local', 'Global', or 'Scheduled'.")

        if isinstance(message_ids, (str, int)):
            message_ids = [str(message_ids)]
        elif isinstance(message_ids, list):
            message_ids = [str(msg_id) for msg_id in message_ids]

        if not message_ids:
            raise InvalidInput("No message IDs provided for deletion.")

        if len(message_ids) > 50:
            chunks = [
                message_ids[i:i + 50]
                for i in range(0, len(message_ids), 50)
            ]

            last_result = None
            for chunk in chunks:
                last_result = await self.request(
                    method = 'deleteMessages',
                    input = {
                        'object_guid': chat_guid,
                        'message_ids': chunk,
                        'type': type
                    }
                )
            return last_result

        return await self.request(
            method = 'deleteMessages',
            input = {
                'object_guid': chat_guid,
                'message_ids': message_ids,
                'type': type
            }
        )