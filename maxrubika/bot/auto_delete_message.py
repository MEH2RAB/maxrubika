import asyncio
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
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
            chat_id (str): Chat ID of the object associated with the message (e.g., user, group, channel).
            message_id (Union[str, int]): The ID of the message to be deleted.
            time (Union[float, int]): The time delay (in seconds) before deleting.

        Returns:
            A status dict confirming the scheduled deletion.
        """
        from ..data import Data

        async def _delete_later():
            await asyncio.sleep(time)
            try:
                await self.delete_message(chat_id, message_id)
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