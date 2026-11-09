from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetJoinLinkUserJoined:
    async def get_join_link_user_joined(
        self: "maxrubika.Messenger",
        chat: str,
        join_link: str,
        all_pages: bool = True,
        start_id: Optional[str] = None
    ):
        """
        Get users who joined via a specific join link.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            join_link (str): The join link (e.g., 'https://rubika.ir/joing/...').
            all_pages (bool, optional): If True, fetch all pages. If False, only one page using start_id. Default is True.
            start_id (str, optional): Pagination start ID. Only used when all_pages is False.

        Returns:
            The result of the API call.
        """
        from ....data import Data
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid group or channel. Expected a valid GUID, link, or username."
            raise InvalidInput(message)

        join_link_lower = join_link.lower()
        if join_link_lower.startswith(('https://rubika.ir/joing/', 'https://rubika.ir/joinc/')):
            hash_link = join_link.split('?')[0].split('#')[0].rstrip('/').split('/')[-1]
        else:
            message = "'join_link' must start with 'https://rubika.ir/joing/' or 'https://rubika.ir/joinc/' and follow the specified hash format."
            raise InvalidInput(message)

        if not all_pages:
            input_data = {
                'object_guid': chat_guid,
                'join_link': hash_link
            }
            if start_id is not None:
                input_data['start_id'] = start_id

            return await self.request(
                method='getJoinLinkUserJoined',
                input=input_data
            )

        total = 0
        all_user_guids = []
        user_guids_set = set()

        while True:
            input_data = {
                'object_guid': chat_guid,
                'join_link': hash_link
            }
            if start_id is not None:
                input_data['start_id'] = start_id

            result = await self.request(
                method='getJoinLinkUserJoined',
                input=input_data
            )

            result_data = Data(result)
            guids = result_data.find_keys('user_guids') or []

            if not guids:
                break

            for guid in guids:
                if guid not in user_guids_set:
                    user_guids_set.add(guid)
                    all_user_guids.append(guid)
                    total += 1

            has_continue = result_data.find_keys('has_continue')
            if not has_continue:
                break

            next_start_id = result_data.find_keys('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {"user_guids": all_user_guids, "total": total}

        return Data(result_dict)