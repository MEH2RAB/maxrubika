from time import time as time
import maxrubika

class GetChatAds:
    async def get_chat_ads(
        self: "maxrubika.Client",
        state: int = round(time()) - 150
    ):
        """
        Retrieves advertising information for chats.

        Parameters:
            state (int, optional): The timestamp state to filter chat ads. 
                Defaults to the current time minus 150 seconds.

        Returns:
            The result of the API call.
        """
        return await self.request(method = 'getChatAds', input = {'state': int(state)})