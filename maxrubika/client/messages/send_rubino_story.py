import random
from typing import Literal
import maxrubika

class SendRubinoStory:
    async def send_rubino_story(
        self: "maxrubika.Client",
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
            type (str): 'Reply' or 'Direct'. Default is 'Reply'.
            is_mute (bool): Send silently without notification. Default is False.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'sendRubinoStory',
            input={
                'object_guid': chat_guid,
                'story_id': story_id,
                'story_profile_id': story_profile_id,
                'reply_text': reply_text,
                'type': type,
                'rnd': random.randint(100000, 999999),
                'is_mute': is_mute
            }
        )