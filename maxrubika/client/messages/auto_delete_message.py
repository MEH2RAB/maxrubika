import asyncio
from typing import Union
import maxrubika

class AutoDeleteMessage:
    async def auto_delete_message(
        self: "maxrubika.Client",
        chat: str,
        message_id: Union[str, int],
        time: Union[float, int]
    ):
        """
        Automatically delete a message after a specified time.

        Parameters:
            chat (str): The GUID, link, or username of the chat associated with the message
                (e.g., user, group, channel).
            message_id (Union[str, int]): The ID of the message to be deleted.
            time (Union[float, int]): The time delay (in seconds) before deleting the message.

        Returns:
            The updated information after deleting the message.
        """
        chat_guid = await self.get_guid(chat)

        await asyncio.sleep(time)
        return await self.delete_messages(chat_guid, message_id)