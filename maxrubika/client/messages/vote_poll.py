from typing import Union
import maxrubika

class VotePoll:
    async def vote_poll(
        self: "maxrubika.Client",
        poll_id: str,
        selection_index: Union[str, int]
    ):
        """
        Vote on a poll option.

        Parameters:
            poll_id (str): The ID of the poll.
            selection_index (Union[str, int]): The index of the option to vote for.

        Returns:
            The update indicating the success of the vote.
        """
        return await self.request(
            method = 'votePoll',
            input = {'poll_id': poll_id, 'selection_index': int(selection_index)})