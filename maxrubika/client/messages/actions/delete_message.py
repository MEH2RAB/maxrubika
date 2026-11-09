from typing import Union, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteMessage:
    async def delete_message(
        self: "maxrubika.Messenger",
        chat: str,
        message_id: Union[str, int],
        type: Literal['Local', 'Global', 'Scheduled'] = 'Global'
    ):
        """
        Delete a single message in a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int]): The ID of the message to delete.
            type (Literal['Local', 'Global', 'Scheduled']): The type of deletion. Case-insensitive. Default is 'Global'.

        Returns:
            The result of the API call.
        """
        return await self.delete_messages(chat, [message_id], type=type)