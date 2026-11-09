from typing import Union, List, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteMessages:
    async def delete_messages(
        self: "maxrubika.Messenger",
        chat: str,
        message_ids: Union[str, int, List[Union[str, int]]],
        type: Literal['Local', 'Global', 'Scheduled'] = 'Global'
    ):
        """
        Delete specified messages associated with the given chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat associated with the messages
                (e.g., user, group, channel).
            message_ids (Union[str, int, List[Union[str, int]]]): The ID or list of IDs of the messages to be deleted.
            type (Literal['Local', 'Global', 'Scheduled']): The type of deletion. Case-insensitive. Default is 'Global'.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        type_map = {
            'global': 'Global',
            'local': 'Local',
            'scheduled': 'Scheduled'
        }
        type = type_map.get(type.lower())

        if not type:
            message = "'type' argument can only be in 'Local', 'Global', or 'Scheduled'."
            raise InvalidInput(message)

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
                input_data = {
                    'object_guid': chat_guid,
                    'message_ids': chunk,
                    'type': type
                }
                last_result = await self.request(
                    method='deleteMessages',
                    input=input_data
                )
            return last_result

        input_data = {
            'object_guid': chat_guid,
            'message_ids': message_ids,
            'type': type
        }

        return await self.request(
            method='deleteMessages',
            input=input_data
        )