import asyncio
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AutoDeleteMessage:
    async def auto_delete_message(
        self: "maxrubika.Messenger",
        chat: str,
        message_id: Union[str, int],
        time: Union[float, int]
    ):
        """
        Automatically delete a message after a specified time.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int]): The ID of the message to be deleted.
            time (Union[float, int]): The time delay (in seconds) before deleting.

        Returns:
            Confirmation of the scheduled deletion
        """
        from ....data import Data

        chat_guid = await self.get_guid(chat)

        async def _delete_later():
            await asyncio.sleep(time)
            try:
                await self.delete_messages(chat_guid, message_id)
            except Exception as e:
                self.logger.warning(f"Auto-delete failed for message {message_id}: {e}")

        asyncio.create_task(_delete_later())

        result_dict = {
            "status": "OK",
            "message": f"Message will be deleted in {time} seconds."
        }

        if getattr(self, 'as_dict', False):
            return result_dict
        return Data(result_dict)