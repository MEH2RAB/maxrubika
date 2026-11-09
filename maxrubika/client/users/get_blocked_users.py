from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetBlockedUsers:
    async def get_blocked_users(
        self: "maxrubika.Messenger",
        show_user_guids: bool = False,
        all_pages: bool = True,
        start_id: Optional[str] = None
    ):
        """
        Get a list of all blocked users.

        Parameters:
            show_user_guids (bool, optional): Show user GUIDs in output. Default is False.
            all_pages (bool, optional): If True, automatically fetch all pages of blocked users. If False, only fetch one page using start_id. Default is True.
            start_id (str, optional): Starting user ID for pagination. Only used when all_pages is False or as the initial point.

        Returns:
            The result containing all blocked users with total count.
        """
        from ...data import Data

        if not all_pages:
            input_data = {'start_id': start_id}

            return await self.request(
                method='getBlockedUsers',
                input=input_data
            )

        total = 0
        all_users = []
        user_guids = set()

        while True:
            input_data = {'start_id': start_id}

            result = await self.request(
                method='getBlockedUsers',
                input=input_data
            )

            if isinstance(result, dict):
                result = Data(result)

            users = result.find_keys('abs_users') or []

            if not users:
                break

            for user in users:
                user_data = Data(user) if isinstance(user, dict) else user
                user_guid = user_data.find_keys('object_guid')

                if user_guid and user_guid not in user_guids:
                    user_guids.add(user_guid)
                    all_users.append(user_data.to_dict())
                    total += 1

            has_continue = result.find_keys('has_continue')
            if not has_continue:
                break

            next_start_id = result.find_keys('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {
            "users": all_users,
            "total": total
        }

        if show_user_guids:
            result_dict["user_guids"] = list(user_guids)

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)