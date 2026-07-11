import maxrubika
from ...data import Data

class GetBlockedUsers:
    async def get_blocked_users(
        self: "maxrubika.Client",
        show_user_guids: bool = False
    ):
        """
        Get a list of all blocked users.

        Parameters:
            show_user_guids (bool, optional): Show user GUIDs in output. Default is False.

        Returns:
            The result containing all blocked users with total count.
        """
        start_id = None
        total = 0
        all_users = []
        user_guids = set()

        while True:
            result = await self.request(
                method = 'getBlockedUsers',
                input = {'start_id': start_id}
            )

            data = result.to_dict() if hasattr(result, 'to_dict') else result

            if not data or not isinstance(data, dict):
                break

            users = data.get('abs_users', [])
            if not users:
                break

            for user in users:
                user_guid = user.get('object_guid')
                if user_guid and user_guid not in user_guids:
                    user_guids.add(user_guid)
                    all_users.append(user)
                    total += 1

            has_continue = data.get('has_continue', False)
            if not has_continue:
                break

            next_start_id = data.get('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {
            "users": all_users,
            "total": total
        }
        if show_user_guids:
            result_dict["user_guids"] = user_guids

        return Data(result_dict)