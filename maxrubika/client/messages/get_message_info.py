from typing import Union
import maxrubika
from ...data import Data

class GetMessageInfo:
    async def get_message_info(
        self: "maxrubika.Client",
        chat: str,
        message_id: Union[str, int]
    ):
        """
        Get detailed information about a message.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int]): The ID of the message to retrieve.

        Returns:
            Message information.
        """
        result = await self.get_messages_by_id(chat, [str(message_id)])

        data = result.to_dict() if hasattr(result, 'to_dict') else result

        msg_list = data.pop("messages", [])
        data["message"] = msg_list[0] if msg_list else None

        return Data ({
            "message": data.pop("message"),
            "timestamp": data.pop("timestamp"),
            **data
        })