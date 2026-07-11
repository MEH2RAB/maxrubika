import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class GetJoinRequests:
    async def get_join_requests(
        self: "maxrubika.Client",
        chat: str,
        show_user_guids: bool = False
    ):
        """
        Get a list of join requests in a channel or group.

        Parameters:
            chat (str): The GUID, link, or username of the channel or group.
            show_user_guids (bool, optional): Show user GUIDs in output. Default is False.

        Returns:
            Data: The result containing all join requests with total count.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        start_id = None
        total = 0
        all_requests = []
        user_guids = []
        seen_guids = set()

        while True:
            result = await self.request(
                method = 'getJoinRequests',
                input = {
                    'object_guid': chat_guid,
                    'start_id': start_id
                }
            )

            data = result.to_dict() if hasattr(result, 'to_dict') else result

            if not data or not isinstance(data, dict):
                break

            join_requests = data.get('join_requests', [])
            if not join_requests:
                break

            for req in join_requests:
                user_guid = req.get('user_guid')
                if user_guid and user_guid not in seen_guids:
                    seen_guids.add(user_guid)
                    user_guids.append(user_guid)
                    all_requests.append(req)
                    total += 1

            has_continue = data.get('has_continue', False)
            if not has_continue:
                break

            next_start_id = data.get('next_start_id')
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

        return Data(result_dict)