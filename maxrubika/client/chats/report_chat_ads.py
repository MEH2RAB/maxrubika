# methods/report_chat_ads.py
import maxrubika

class ReportChatAds:
    async def report_chat_ads(
        self: "maxrubika.Client",
        chat_ads_id: str
    ):
        """
        Register a report action on a chat ad.

        The `chat_ads_id` is obtained from the `get_chat_ads` method.

        Parameters:
            chat_ads_id (str): The chat ads ID to report.

        Returns:
            The result of the operation.
        """
        return await self.request(
            method = 'actionOnChatAds',
            input = {
                'chat_ads_id': chat_ads_id,
                'action': 'Report'
            }
        )