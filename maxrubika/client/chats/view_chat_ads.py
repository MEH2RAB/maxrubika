import maxrubika

class ViewChatAds:
    async def view_chat_ads(
        self: "maxrubika.Client",
        chat_ads_id: str
    ):
        """
        Register a view action on a chat ad.

        The `chat_ads_id` is obtained from the `get_chat_ads` method.

        Parameters:
            chat_ads_id (str): The chat ads ID to register a view on.

        Returns:
            The result of the operation.
        """
        return await self.request(
            method = 'actionOnChatAds',
            input = {
                'chat_ads_id': chat_ads_id,
                'action': 'View'
            }
        )