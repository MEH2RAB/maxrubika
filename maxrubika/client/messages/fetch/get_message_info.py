from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMessageInfo:
    async def get_message_info(
        self: "maxrubika.Messenger",
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
        from ....data import Data

        result = await self.get_messages_by_id(chat, [str(message_id)])

        if isinstance(result, dict):
            result = Data(result)

        msg_list = result.find_keys('messages') or []
        timestamp = result.find_keys('timestamp')

        data = result.to_dict()
        data.pop("messages", None)
        data.pop("client", None)

        message = msg_list[0] if msg_list else None

        if isinstance(message, dict):
            message = Data(message)

        result_dict = {
            "message": message,
            "timestamp": timestamp,
            **data
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)