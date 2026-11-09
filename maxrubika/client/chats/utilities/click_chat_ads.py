from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ClickChatAds:
    async def click_chat_ads(
        self: "maxrubika.Messenger",
        chat_ads_id: str
    ):
        """
        Register a click action on a chat ad.

        The `chat_ads_id` is obtained from the `get_chat_ads` method.

        Parameters:
            chat_ads_id (str): The chat ads ID to register a click on.

        Returns:
            The result of the operation.
        """
        input_data = {
            'chat_ads_id': chat_ads_id,
            'action': 'Click'
        }

        return await self.request(method='actionOnChatAds', input=input_data)