import maxrubika

class GetLivePlayUrl:
    async def get_live_play_url(
        self: "maxrubika.Client",
        access_token: str,
        live_id: str
    ):
        """
        Retrieves the play URL for a live stream.

        Parameters:
            access_token (str): The access token for authentication.
            live_id (str): The ID of the live stream.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'getLivePlayUrl',
            input = {
                'access_token': access_token,
                'live_id': live_id
            }
        )