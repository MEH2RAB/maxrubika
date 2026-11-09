from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendNowScheduledMessage:
    async def send_now_scheduled_message(
        self: "maxrubika.Messenger",
        chat: str,
        message_id: Union[int, str]
    ):
        """
        Send a scheduled message immediately.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[int, str]): The ID of the scheduled message to send now.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {
            'object_guid': chat_guid,
            'message_id': message_id
        }

        return await self.request(method='sendNowScheduledMessage', input=input_data)