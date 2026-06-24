from typing import Union
import asyncio
import maxrubika

class AutoDeleteMessage:
    async def auto_delete_message(
        self: "maxrubika.Bot",
        chat_id: str,
        message_id: Union[str, int],
        time: Union[float, int]
    ):
        """
        Automatically delete a message after a specified time.

        Parameters:
            chat_id (str): chat_id of the object associated with the message (e.g., user, group, channel).
            message_id (str): The ID of the message to be deleted.
            time (Union[float, int]): The time delay (in seconds) before deleting the message.

        Returns:
            The updated information after deleting the message.
        """
        await asyncio.sleep(time)
        return await self.delete_message(chat_id, message_id)