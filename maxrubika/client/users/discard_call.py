from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DiscardCall:
    async def discard_call(
        self: "maxrubika.Messenger",
        call_id: str,
        duration: int = 0,
        reason: Literal['Missed', 'Disconnect', 'Hangup', 'Busy'] = 'Disconnect'
    ):
        """
        Discard/end an active call.

        Parameters:
            call_id (str): ID of the call to discard
            duration (int): Call duration in seconds. Default: 0
            reason (Literal['Missed', 'Disconnect', 'Hangup', 'Busy']): Reason for ending the call. Case-insensitive. Default: 'Disconnect'

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

        reason_map = {
            'missed': 'Missed',
            'disconnect': 'Disconnect',
            'hangup': 'Hangup',
            'busy': 'Busy',
        }
        reason = reason_map.get(reason.lower())

        if not reason:
            message = "'reason' must be one of 'Missed', 'Disconnect', 'Hangup', or 'Busy'."
            raise InvalidInput(message)

        input_data = {
            'call_id': call_id,
            'duration': duration,
            'reason': reason
        }

        return await self.request(
            method='discardCall',
            input=input_data
        )