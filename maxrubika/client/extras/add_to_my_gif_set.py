from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AddToMyGifSet:
    async def add_to_my_gif_set(
        self: "maxrubika.Messenger",
        chat: str,
        message_id: Union[str, int]
    ):
        """
        Adds a GIF message to the user's personal GIF set.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int]): The ID of the GIF message.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {'object_guid': chat_guid, 'message_id': message_id}
        return await self.request(
            method='addToMyGifSet',
            input=input_data
        )