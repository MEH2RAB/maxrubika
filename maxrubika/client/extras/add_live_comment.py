from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AddLiveComment:
    async def add_live_comment(
        self: "maxrubika.Messenger",
        live_id: str,
        access_token: str,
        comment: str
    ):
        """
        Adds a comment to a live stream.

        Parameters:
            live_id (str): The ID of the live stream.
            access_token (str): The access token for authentication.
            comment (str): The text of the comment.

        Returns:
            The result of the API call.
        """
        input_data = {
            'live_id': live_id,
            'access_token': access_token,
            'text': comment
        }
        return await self.request(
            method='addLiveComment',
            input=input_data
        )