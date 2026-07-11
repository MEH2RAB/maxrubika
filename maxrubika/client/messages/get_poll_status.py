import maxrubika

class GetPollStatus:
    async def get_poll_status(self: "maxrubika.Client", poll_id: str):
        """
        Get the status of a specific poll.

        Parameters:
            poll_id (str): The ID of the poll for which the status is requested.

        Returns:
            The status of the specified poll.
        """
        return await self.request(method = 'getPollStatus', input = {'poll_id': poll_id})
