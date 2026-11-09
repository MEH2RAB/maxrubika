from typing import Literal, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetLiveStatus:
    async def get_live_status(
        self: "maxrubika.Messenger",
        live_id: str,
        access_token: str,
        type: Optional[Literal["LiveViewer", "MessageStat"]] = None
    ):
        """
        Get live stream status.

        Parameters:
            live_id (str): Live stream ID.
            access_token (str): Access token from send_live response.
            type (Literal["LiveViewer", "MessageStat"], optional): Type of status to retrieve ('LiveViewer' for viewer statistics, 'MessageStat' for message/comment statistics). If not provided, defaults to server behavior (usually LiveViewer).

        Returns:
            Live status info.
        """
        from ..exceptions import InvalidInput

        if type is not None:
            type_map = {
                "liveviewer": "LiveViewer",
                "messagestat": "MessageStat"
            }
            type = type_map.get(type.lower())

            if not type:
                raise InvalidInput("'type' must be 'LiveViewer' or 'MessageStat'.")

        input_data = {
            'live_id': live_id,
            'access_token': access_token
        }

        if type is not None:
            input_data['type'] = type

        return await self.request(
            method='getLiveStatus',
            input=input_data
        )