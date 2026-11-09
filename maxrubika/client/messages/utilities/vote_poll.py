from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class VotePoll:
    async def vote_poll(
        self: "maxrubika.Messenger",
        poll_id: str,
        selection_index: Union[str, int]
    ):
        """
        Vote on a poll option.

        Parameters:
            poll_id (str): The ID of the poll.
            selection_index (Union[str, int]): The index of the option to vote for.

        Returns:
            The result of the API call.
        """
        input_data = {
            'poll_id': poll_id,
            'selection_index': int(selection_index)
        }

        return await self.request(
            method='votePoll',
            input=input_data
        )