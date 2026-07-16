from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class SendNowScheduledMessage:
    async def send_now_scheduled_message(
        self: "maxrubika.Client",
        chat: str,
        message_id: Union[int, str]
    ):
        """
        Send a scheduled message immediately.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (int): The ID of the scheduled message to send now.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'sendNowScheduledMessage',
            input = {
                'object_guid': chat_guid,
                'message_id': message_id
            }
        )