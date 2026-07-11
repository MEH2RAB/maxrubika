import typing
import maxrubika

class ClickMessageUrl:
    async def click_message_url(
        self: "maxrubika.Client",
        chat: str,
        message_id: typing.Union[str, int],
        link_url: str
    ):
        """
        Simulate clicking a URL contained within a specific message.

        Parameters:
            chat (str): The GUID, link or username of the chat.
            message_id (Union[str, int]): The unique ID of the message that includes the URL.
            link_url(str): The URL string embedded in the message to be clicked.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'clickMessageUrl',
            input = {
                'object_guid': chat_guid,
                'message_id': message_id,
                'link_url': link_url
            }
        )