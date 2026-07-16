import maxrubika

class StopPoll:
    async def stop_poll(
        self: "maxrubika.Client",
        poll_id: str
    ):
        """
        Stop a poll.

        Parameters:
            poll_id (str): The ID of the poll to stop.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'setPollAction',
            input = {
                'poll_id': poll_id,
                'action': 'Stop'
            }
        )