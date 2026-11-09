from typing import Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteMessages:
    async def delete_messages(
        self: "maxrubika.Bot",
        chat_id: str,
        message_ids: Union[int, str, List[Union[int, str]]]
    ):
        """
        Delete one or more messages.

        Parameters:
            chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0') or user (starts with 'b0').
            message_ids (Union[int, str, List[Union[int, str]]]): A single message ID or a list of message IDs to delete.

        Returns:
            A list of API responses, one for each message.
        """
        from .exceptions import InvalidInput

        if not isinstance(message_ids, list):
            message_ids = [message_ids]

        if not message_ids:
            raise InvalidInput("'message_ids' must not be empty.")

        results = []
        for message_id in message_ids:
            result = await self.delete_message(chat_id, message_id)
            results.append(result)

        return results