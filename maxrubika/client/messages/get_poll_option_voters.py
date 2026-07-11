from typing import Union, Optional
import maxrubika

class GetPollOptionVoters:
    async def get_poll_option_voters(
        self: "maxrubika.Client",
        poll_id: str,
        selection_index: Union[str, int],
        start_id: Optional[str] = None
    ):
        """
        Get voters for a specific poll option.

        Parameters:
            poll_id (str): The ID of the poll for which voters are requested.
            selection_index (Union[str, int]): The index of the poll option for which voters are requested.
            start_id (Optional[str]): The ID from which to start fetching voters. Defaults to None.

        Returns:
            The voters for the specified poll option.
        """
        input = {
            'poll_id': poll_id,
            'selection_index': selection_index,
            'start_id': start_id
        }
        return await self.request(method = 'getPollOptionVoters', input = input)