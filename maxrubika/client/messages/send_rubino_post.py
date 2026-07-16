import random
import maxrubika

class SendRubinoPost:
    async def send_rubino_post(
        self: "maxrubika.Client",
        chat: str,
        post_id: str,
        post_profile_id: str,
        is_mute: bool = False
    ):
        """
        Send a Rubino post to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            post_id (str): The post ID to send.
            post_profile_id (str): The post profile ID.
            is_mute (bool): Send silently without notification. Default is False.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'sendRubinoPost',
            input = {
                'object_guid': chat_guid,
                'post_id': post_id,
                'post_profile_id': post_profile_id,
                'rnd': random.randint(100000, 999999),
                'is_mute': is_mute
            }
        )