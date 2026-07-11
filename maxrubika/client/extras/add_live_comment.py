import maxrubika

class AddLiveComment:
    async def add_live_comment(
        self: "maxrubika.Client",
        access_token: str,
        live_id: str,
        comment: str
    ):
        """
        Adds a comment to a live stream.

        Parameters:
            access_token (str): The access token for authentication.
            live_id (str): The ID of the live stream.
            comment (str): The text of the comment.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'addLiveComment',
            input = {
                'access_token': access_token,
                'live_id': live_id,
                'text': comment
            }
        )