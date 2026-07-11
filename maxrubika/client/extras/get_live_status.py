import maxrubika

class GetLiveStatus:
    async def get_live_status(
        self: "maxrubika.Client",
        live_id: str,
        access_token: str
    ):
        """
        Get live stream status.

        Parameters:
            live_id (str): Live stream ID.
            access_token (str): Access token from send_live response.

        Returns:
            Live status info.
        """
        return await self.request(
            method = 'getLiveStatus',
            input = {
                'live_id': live_id,
                'access_token': access_token
                }
            )