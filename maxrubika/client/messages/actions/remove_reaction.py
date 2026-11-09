from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class RemoveReaction:
    async def remove_reaction(
        self: "maxrubika.Messenger",
        chat: str,
        message_id: Union[str, int],
        reaction_id: Union[int, str]
    ):
        """
        Remove a reaction from a specific message.

        Parameters:
            chat (str): The GUID, link, or username of the chat associated with the message.
            message_id (Union[str, int]): The ID of the message from which the reaction will be removed.
            reaction_id (Union[int, str]): The ID of the reaction to be removed.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {
            'object_guid': chat_guid,
            'message_id': message_id,
            'reaction_id': reaction_id,
            'action': 'Remove'
        }

        return await self.request(method='actionOnMessageReaction', input=input_data)