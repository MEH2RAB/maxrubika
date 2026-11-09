from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetLiveSetting:
    async def set_live_setting(
        self: "maxrubika.Messenger",
        live_id: str,
        title: Optional[str] = None,
        allow_comment: Optional[bool] = None
    ):
        """
        Update settings for a live stream.

        Parameters:
            live_id (str): Live stream ID.
            title (str, optional): New title for the live stream.
            allow_comment (bool, optional): Whether to allow comments on the live stream.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

        if title is None and allow_comment is None:
            message = "At least one parameter (title, allow_comment) should be provided for update."
            raise InvalidInput(message)

        input_data = {
            'live_id': live_id,
            'updated_parameters': []
        }

        if title is not None:
            input_data['updated_parameters'].append('title')
            input_data['title'] = title

        if allow_comment is not None:
            input_data['updated_parameters'].append('allow_comment')
            input_data['allow_comment'] = allow_comment

        return await self.request(
            method='setLiveSetting',
            input=input_data
        )