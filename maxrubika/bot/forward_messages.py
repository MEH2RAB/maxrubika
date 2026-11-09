from typing import Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ForwardMessages:
    async def forward_messages(
        self: "maxrubika.Bot",
        from_chat_id: str,
        message_ids: Union[int, str, List[Union[int, str]]],
        to_chat_id: str,
        disable_notification: bool = False
    ):
        """
        Forward one or more messages from one chat to another.

        Parameters:
            from_chat_id (str): chat_id of the source object from which messages are forwarded.
            message_ids (Union[int, str, List[Union[int, str]]]): A single message ID or a list of message IDs to forward.
            to_chat_id (str): chat_id of the destination object to which messages are forwarded.
            disable_notification (bool): If set to True, the messages will be sent silently without triggering a notification for users. Defaults to False.

        Returns:
            API responses, one for each forwarded message.
        """
        from .exceptions import InvalidInput

        if not isinstance(message_ids, list):
            message_ids = [message_ids]

        if not message_ids:
            raise InvalidInput("'message_ids' must not be empty.")

        results = []
        for message_id in message_ids:
            result = await self.forward_message(
                from_chat_id=from_chat_id,
                message_id=message_id,
                to_chat_id=to_chat_id,
                disable_notification=disable_notification
            )
            results.append(result)

        return results