from typing import Union
import maxrubika

class RemoveReaction:
    async def remove_reaction(
        self: "maxrubika.Client",
        chat: str,
        message_id: Union[str, int],
        reaction_id: Union[int, str]
    ):
        """
        Remove a reaction from a specific message.

        Parameters:
            chat (str): The GUID, link, or username of the chat associated with the message.
            message_id (str): The ID of the message from which the reaction will be removed.
            reaction_id (int): The ID of the reaction to be removed.

        Returns:
            The update indicating the success of removing the reaction.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'actionOnMessageReaction',
            input = {
                'object_guid': chat_guid,
                'message_id': message_id,
                'reaction_id': reaction_id,
                'action': 'Remove'
                }
            )