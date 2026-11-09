from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class RateCall:
    async def rate_call(
        self: "maxrubika.Messenger",
        call_id: str,
        star_count: int,
        comment: Optional[str] = None
    ):
        """
        Rate a call.

        Parameters:
            call_id (str): The ID of the call to rate.
            star_count (int): Rating stars (usually 1 to 5).
            comment (str, optional): Optional comment about the call. Defaults to None.

        Returns:
            The result of the API call.
        """
        input_data = {
            'call_id': call_id,
            'star_count': star_count
        }

        if comment is not None:
            input_data['comment'] = comment

        return await self.request(
            method='rateCall',
            input=input_data
        )