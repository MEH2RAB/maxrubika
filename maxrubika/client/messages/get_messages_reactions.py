from typing import Union
import maxrubika

class GetMessagesReactions:
    async def get_messages_reactions(
        self: "maxrubika.Client",
        chat: str,
        min_id: Union[str, int],
        max_id: Union[str, int]
    ):
        """
        Get reactions of messages in a chat within a specific ID range.

        Parameters:
            chat (str): Chat identifier (link, username, or GUID)
            min_id (Union[str, int]): Minimum message ID (lower bound)
            max_id (Union[str, int]): Maximum message ID (upper bound)

        Returns:
            List of reactions for messages in the specified range.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'getChatReaction',
            input = {
                'object_guid': chat_guid,
                'min_id': min_id,
                'max_id': max_id
            }
        )