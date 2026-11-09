from typing import Union, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AcceptAllJoinRequests:
    async def accept_all_join_requests(
        self: "maxrubika.Messenger",
        chat: str,
        exclude: Optional[Union[str, List[str]]] = None
    ):
        """
        Accept all pending join requests in a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the group or channel.
            exclude (Optional[Union[str, List[str]]]): User GUID(s) or username(s) to exclude.

        Returns:
            Result containing accepted count and details.
        """
        from ....data import Data
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        join_requests = await self.get_join_requests(chat_guid, show_user_guids=True)

        if isinstance(join_requests, dict):
            join_requests = Data(join_requests)

        user_guids = join_requests.find_keys('user_guids') or []
        total_requests = len(user_guids)

        if not user_guids:
            result_dict = {
                "status": "OK",
                "message": "No pending join requests found.",
                "total_requests": 0
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        exclude_guids = []
        if exclude:
            if isinstance(exclude, str):
                exclude = [exclude]
            for item in exclude:
                try:
                    guid = await self.get_guid(item)
                    if guid.startswith("u0"):
                        exclude_guids.append(guid)
                except Exception:
                    pass

        filtered_guids = [g for g in reversed(user_guids) if g not in exclude_guids]

        if not filtered_guids:
            result_dict = {
                "status": "OK",
                "message": "All requests are excluded.",
                "total_requests": total_requests,
                "excluded_count": len(exclude_guids)
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        failed_count = 0
        for user_guid in filtered_guids:
            try:
                await self.accept_join_request(chat_guid, user_guid)
            except Exception:
                failed_count += 1

        result_dict = {
            "status": "OK",
            "accepted_count": len(filtered_guids) - failed_count,
            "failed_count": failed_count,
            "total_requests": total_requests,
            "excluded_count": len(exclude_guids)
        }
        if getattr(self, 'as_dict', False):
            return result_dict
        return Data(result_dict)