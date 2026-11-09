from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetLiveComments:
    async def get_live_comments(
        self: "maxrubika.Messenger",
        live_id: str,
        access_token: str,
        start_id: Optional[str] = None
    ):
        """
        Get live stream comments.

        Parameters:
            live_id (str): Live stream ID.
            access_token (str): Access token from send_live response.
            start_id (str, optional): The starting comment ID to fetch comments from. Defaults to None.

        Returns:
            The result of the API call.
        """
        input_data = {
            'live_id': live_id,
            'access_token': access_token
        }
        
        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getLiveComments',
            input=input_data
        )