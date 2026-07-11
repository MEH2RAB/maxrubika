import random
from typing import Union
import maxrubika

class ForwardMessages:
    async def forward_messages(
        self: "maxrubika.Client",
        from_chat: str,
        message_ids: Union[str, int, list],
        to_chat: str
    ):
        """
        Forward specified messages from one chat to another.

        Parameters:
            from_chat (str): The GUID, link, or username of the source chat from which messages are forwarded.
            message_ids (Union[str, int, list]): The IDs of the messages to be forwarded.
                Can be a single ID or a list of IDs.
            to_chat (str): The GUID, link, or username of the destination chat to which messages are forwarded.

        Returns:
            The updated information after forwarding the messages.
        """
        from_chat_guid = await self.get_guid(from_chat)
        to_chat_guid = await self.get_guid(to_chat)

        if not isinstance(message_ids, list):
            message_ids = [message_ids]

        return await self.request(
            method = 'forwardMessages',
            input = {
                'from_object_guid': from_chat_guid,
                'to_object_guid': to_chat_guid,
                'message_ids': message_ids,
                'rnd': random.randint(100000, 999999)
            }
        )