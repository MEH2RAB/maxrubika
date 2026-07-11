import maxrubika
from typing import Union, List, Optional
from ...data import Data
from ..exceptions import InvalidInput

class AcceptAllJoinRequests:
    async def accept_all_join_requests(
        self: "maxrubika.Client",
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
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        join_requests = await self.get_join_requests(chat_guid, show_user_guids=True)
        requests_data = join_requests.to_dict() if hasattr(join_requests, 'to_dict') else join_requests

        user_guids = requests_data.get('user_guids', [])
        total_requests = len(user_guids)

        if not user_guids:
            return Data({"status": "OK", "message": "No pending join requests found."})

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
            return Data({
                "status": "OK",
                "message": "All requests are excluded.",
                "total_requests": total_requests,
                "excluded_count": len(exclude_guids)
            })

        failed_count = 0
        for user_guid in filtered_guids:
            try:
                await self.accept_join_request(chat_guid, user_guid)
            except Exception:
                failed_count += 1

        return Data({
            "status": "OK",
            "accepted_count": len(filtered_guids) - failed_count,
            "failed_count": failed_count,
            "total_requests": total_requests,
            "excluded_count": len(exclude_guids)
        })