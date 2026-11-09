from typing import Union, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UnblockAllUsers:
    async def unblock_all_users(
        self: "maxrubika.Messenger",
        exclude: Optional[Union[str, List[str]]] = None
    ):
        """
        Unblock all blocked users.

        Parameters:
            exclude (Union[str, List[str]], optional): User GUID(s) or username(s) to exclude from unblock. Default is None.

        Returns:
            Result of unblock operation.
        """
        from ...data import Data
        from ..exceptions import InvalidInput

        blocked_result = await self.get_blocked_users(show_user_guids=True)

        if isinstance(blocked_result, dict):
            blocked_result = Data(blocked_result)

        blocked_guids = blocked_result.find_keys('user_guids') or []

        if not blocked_guids:
            no_blocked = {"status": "OK", "message": "No blocked users found."}
            if getattr(self, 'as_dict', False):
                return no_blocked
            return Data(no_blocked)

        exclude_list = []
        if exclude is not None:
            if isinstance(exclude, str):
                exclude_list.append(exclude)
            elif isinstance(exclude, list):
                exclude_list.extend(exclude)

        exception_guids = []

        if exclude_list:
            for user in exclude_list:
                user_guid = await self.get_guid(user)

                if not user_guid.startswith(("u0", "b0")):
                    message = f"'{user}' does not point to a valid user or bot. Expected a user GUID, bot GUID, or username."
                    raise InvalidInput(message)

                exception_guids.append(user_guid)

        final_guids = [guid for guid in blocked_guids if guid not in exception_guids]

        if not final_guids:
            all_excluded = {
                "status": "OK",
                "message": "All blocked users are in exceptions list. No one to unblock."
            }
            if getattr(self, 'as_dict', False):
                return all_excluded
            return Data(all_excluded)

        total = len(blocked_guids)
        excluded = len(exception_guids)

        failed_count = 0
        for user_guid in final_guids:
            try:
                await self.unblock_user(user_guid)
            except Exception:
                failed_count += 1

        result_dict = {
            "status": "OK",
            "total_blocked": total,
            "excluded": excluded,
            "unblocked": len(final_guids) - failed_count,
            "failed": failed_count
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)