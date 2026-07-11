from typing import Union
import maxrubika

class GetMessageUrl:
    async def get_message_url(
        self: "maxrubika.Client",
        chat: str,
        message_id: Union[str, int]
    ):
        """
        Get the shareable URL of a specific message.

        Parameters:
            chat (str): The GUID, link, or username of the chat to which the message belongs.
            message_id (Union[str, int]): The ID of the message for which to retrieve the shareable URL.

        Returns:
            The shareable URL of the specified message.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'getMessageShareUrl',
            input = {
                'object_guid': chat_guid,
                'message_id': message_id
            }
        )