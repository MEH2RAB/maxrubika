from typing import Union
import maxrubika

class AddReaction:
    async def add_reaction(
        self: "maxrubika.Client",
        chat: str,
        message_id: Union[str, int],
        reaction_id: Union[int, str]
    ):
        """
        Add a reaction to a specific message.

        Parameters:
            chat (str): The GUID, link, or username of the chat associated with the message.
            message_id (Union[str, int]): The ID of the message to which the reaction will be added.
            reaction_id (Union[str, int]): The ID of the reaction to be added.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'actionOnMessageReaction',
            input = {
                'object_guid': chat_guid,
                'message_id': message_id,
                'reaction_id': reaction_id,
                'action': 'Add'
                }
            )