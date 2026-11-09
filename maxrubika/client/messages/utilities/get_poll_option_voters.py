from typing import Union, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPollOptionVoters:
    async def get_poll_option_voters(
        self: "maxrubika.Messenger",
        poll_id: str,
        selection_index: Union[str, int],
        show_user_guids: bool = False,
        all_pages: bool = True,
        start_id: Optional[str] = None
    ):
        """
        Get voters for a specific poll option.

        Parameters:
            poll_id (str): The ID of the poll for which voters are requested.
            selection_index (Union[str, int]): The index of the poll option for which voters are requested.
            show_user_guids (bool, optional):
                If True, include a list of unique voter GUIDs in the output.
                Default is False.
            all_pages (bool, optional):
                If True, automatically fetch all pages of voters.
                If False, only fetch one page using start_id.
                Default is True.
            start_id (Optional[str]): The ID from which to start fetching voters.
                Only used when all_pages is False or as the initial point.

        Returns:
            Result containing all voters, total count, and optionally voter_guids.
        """
        from ....data import Data

        if not all_pages:
            input_data = {
                'poll_id': poll_id,
                'selection_index': selection_index
            }
            if start_id is not None:
                input_data['start_id'] = start_id

            return await self.request(
                method='getPollOptionVoters',
                input=input_data
            )

        total = 0
        all_voters = []
        voter_guids = set()

        while True:
            input_data = {
                'poll_id': poll_id,
                'selection_index': selection_index
            }
            if start_id is not None:
                input_data['start_id'] = start_id

            result = await self.request(
                method='getPollOptionVoters',
                input=input_data
            )

            if isinstance(result, dict):
                result = Data(result)

            voters = result.find_keys('voters_abs_objects') or []

            if not voters:
                break

            for voter in voters:
                voter_data = Data(voter) if isinstance(voter, dict) else voter
                voter_guid = voter_data.find_keys('object_guid')

                if voter_guid and voter_guid not in voter_guids:
                    voter_guids.add(voter_guid)
                    all_voters.append(voter_data.to_dict())
                    total += 1

            has_continue = result.find_keys('has_continue')
            if not has_continue:
                break

            next_start_id = result.find_keys('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {
            "voters": all_voters,
            "total": total
        }

        if show_user_guids:
            result_dict["voter_guids"] = list(voter_guids)

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)