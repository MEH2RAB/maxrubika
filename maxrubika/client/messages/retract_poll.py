import maxrubika

class RetractPoll:
    async def retract_poll(
        self: "maxrubika.Client",
        poll_id: str
    ):
        """
        Retract a poll.

        Parameters:
            poll_id (str): The ID of the poll to retract.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'setPollAction',
            input = {
                'poll_id': poll_id,
                'action': 'Retract'
            }
        )