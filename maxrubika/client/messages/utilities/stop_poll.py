from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class StopPoll:
    async def stop_poll(
        self: "maxrubika.Messenger",
        poll_id: str
    ):
        """
        Stop a poll.

        Parameters:
            poll_id (str): The ID of the poll to stop.

        Returns:
            The result of the API call.
        """
        input_data = {
            'poll_id': poll_id,
            'action': 'Stop'
        }

        return await self.request(method='setPollAction', input=input_data)