import maxrubika

class GetLiveComments:
    async def get_live_comments(
        self: "maxrubika.Client",
        live_id: str,
        access_token: str
    ):
        """
        Get live stream comments.

        Parameters:
            live_id (str): Live stream ID.
            access_token (str): Access token from send_live response.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'getLiveComments',
            input = {
                'live_id': live_id,
                'access_token': access_token
                }
            )