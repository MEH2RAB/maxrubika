from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetLivePlayUrl:
    async def get_live_play_url(
        self: "maxrubika.Messenger",
        live_id: str,
        access_token: str
    ):
        """
        Retrieves the play URL for a live stream.

        Parameters:
            live_id (str): The ID of the live stream.
            access_token (str): The access token for authentication.

        Returns:
            The result of the API call.
        """
        input_data = {
            'live_id': live_id,
            'access_token': access_token
        }

        return await self.request(
            method='getLivePlayUrl',
            input=input_data
        )