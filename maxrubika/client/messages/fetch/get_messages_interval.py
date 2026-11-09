from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMessagesInterval:
    async def get_messages_interval(
        self: "maxrubika.Messenger",
        chat: str,
        middle_message_id: Union[int, str]
    ):
        """
        Retrieve messages in an interval around a middle message ID.

        Parameters:
            chat (str): The GUID, link, or username of the chat to which the messages belong.
            middle_message_id (Union[int, str]): The middle message ID around which the interval is determined.

        Returns:
            The retrieved messages in the specified interval.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {
            'object_guid': chat_guid,
            'middle_message_id': middle_message_id
        }

        return await self.request(method='getMessagesInterval', input=input_data)