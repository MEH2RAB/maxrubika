import random
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendRubinoStory:
    async def send_rubino_story(
        self: "maxrubika.Messenger",
        chat: str,
        story_id: str,
        story_profile_id: str,
        reply_text: str = "",
        type: Literal['Reply', 'Direct'] = 'Reply',
        is_mute: bool = False
    ):
        """
        Send a Rubino story reply or direct message.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            story_id (str): The story ID.
            story_profile_id (str): The story profile ID.
            reply_text (str): Reply text. Default is empty string.
            type (str): 'Reply' or 'Direct'. Case-insensitive. Default is 'Reply'.
            is_mute (bool): Send silently without notification. Default is False.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        type_map = {
            'reply': 'Reply',
            'direct': 'Direct'
        }
        normalized_type = type_map.get(str(type).lower())

        if not normalized_type:
            message = "'type' must be 'Reply' or 'Direct'."
            raise InvalidInput(message)

        input_data = {
            'object_guid': chat_guid,
            'story_id': story_id,
            'story_profile_id': story_profile_id,
            'reply_text': reply_text,
            'type': normalized_type,
            'rnd': random.randint(100000, 999999),
            'is_mute': is_mute
        }

        return await self.request(method='sendRubinoStory', input=input_data)