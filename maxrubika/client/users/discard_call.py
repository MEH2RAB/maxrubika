import maxrubika

class DiscardCall:
    async def discard_call(
        self: "maxrubika.Client",
        call_id: str,
        duration: int,
        reason: str = "Disconnect"
    ):
        """
        Discard/end an active call.

        Parameters:
            call_id (str): ID of the call to discard
            duration (int): Call duration in seconds
            reason (str): Reason for ending the call.
                Common options: 'Missed' and 'Disconnect'.
                Default: 'Disconnect'

        Returns:
            Result of the discard operation.
        """
        return await self.request(
            method = 'discardCall',
            input = {
                'call_id': call_id,
                'duration': duration,
                'reason': reason
            }
        )