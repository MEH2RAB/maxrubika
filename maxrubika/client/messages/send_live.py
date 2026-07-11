from typing import Union
import random
import maxrubika

class SendLive:
    async def send_live(
        self: "maxrubika.Client",
        chat: str,
        title: str = "Live stream",
        reply_to_message_id: Union[str, int] = None,
        thumbnail: str = None
    ):
        """
        Send a live stream.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            title (str): Live stream title.
            reply_to_message_id (Optional[Union[str, int]]): The ID of the message to which this is a reply. Defaults to None.
            thumbnail (str): Base64 encoded thumbnail image.
                If not provided, a default thumbnail will be used.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if thumbnail is None:
            thumbnail = "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"

        return await self.request(
            method = 'sendLive',
            input = {
                'object_guid': chat_guid,
                'title': title,
                'device_type': 'Software',
                'thumb_inline': thumbnail,
                'rnd': random.randint(100000, 999999),
                'reply_to_message_id': reply_to_message_id
                }
            )