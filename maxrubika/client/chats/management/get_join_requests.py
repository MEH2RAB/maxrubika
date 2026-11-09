from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetJoinRequests:
    async def get_join_requests(
        self: "maxrubika.Messenger",
        chat: str,
        show_user_guids: bool = False,
        search_text: Optional[str] = None,
        join_link: Optional[str] = None,
        all_pages: bool = True,
        start_id: Optional[str] = None
    ):
        """
        Get a list of join requests in a channel or group.

        Parameters:
            chat (str): The GUID, link, or username of the channel or group.
            show_user_guids (bool, optional): Show user GUIDs in output. Default is False.
            search_text (str, optional): Search text to filter requests. Defaults to None.
            join_link (str, optional): Filter requests by a specific join link.
            all_pages (bool, optional):
                If True, automatically fetch all pages of join requests.
                If False, only fetch one page using start_id.
                Default is True.
            start_id (str, optional):
                Starting request ID for pagination.
                Only used when all_pages is False.

        Returns:
            Data or dict: The result containing all join requests with total count.
        """
        from ....data import Data
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        if search_text is not None:
            search_text = search_text.replace("@", "")

        hash_link = None
        if join_link is not None:
            join_link_lower = join_link.lower()
            if join_link_lower.startswith(('https://rubika.ir/joing/', 'https://rubika.ir/joinc/')):
                hash_link = join_link.split('?')[0].split('#')[0].rstrip('/').split('/')[-1]
            else:
                message = "'join_link' must start with 'https://rubika.ir/joing/' or 'https://rubika.ir/joinc/' and follow the specified hash format."
                raise InvalidInput(message)

        if not all_pages:
            input_data = {'object_guid': chat_guid}
            if search_text is not None:
                input_data['search_text'] = search_text
            if hash_link is not None:
                input_data['join_link'] = hash_link
            if start_id is not None:
                input_data['start_id'] = start_id

            return await self.request(
                method='getJoinRequests',
                input=input_data
            )

        total = 0
        all_requests = []
        user_guids = []
        seen_guids = set()

        while True:
            input_data = {'object_guid': chat_guid}
            if search_text is not None:
                input_data['search_text'] = search_text
            if hash_link is not None:
                input_data['join_link'] = hash_link
            if start_id is not None:
                input_data['start_id'] = start_id

            result = await self.request(
                method='getJoinRequests',
                input=input_data
            )

            if isinstance(result, dict):
                result = Data(result)

            join_requests = result.find_keys('join_requests') or []

            if not join_requests:
                break

            for req in join_requests:
                if isinstance(req, dict):
                    req = Data(req)

                user_guid = req.find_keys('user_guid')
                if user_guid and user_guid not in seen_guids:
                    seen_guids.add(user_guid)
                    user_guids.append(user_guid)
                    all_requests.append(req.to_dict())
                    total += 1

            has_continue = result.find_keys('has_continue')
            if not has_continue:
                break

            next_start_id = result.find_keys('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {
            "join_requests": all_requests,
            "total": total,
            "chat_guid": chat_guid
        }
        if show_user_guids:
            result_dict["user_guids"] = user_guids

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)