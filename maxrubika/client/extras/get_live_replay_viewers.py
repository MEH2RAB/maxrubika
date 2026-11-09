from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetLiveReplayViewers:
    async def get_live_replay_viewers(
        self: "maxrubika.Messenger",
        live_id: str,
        start_id: Optional[str] = None
    ):
        """
        Get the list of replay (VOD) viewers for a live stream.

        Parameters:
            live_id (str): Live stream ID.
            start_id (str, optional): The starting viewer ID for pagination. Defaults to None.

        Returns:
            The result of the API call, containing a list of replay viewers.
        """
        input_data = {
            'live_id': live_id,
            'type': 'VOD'
        }

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getLiveViewers',
            input=input_data
        )