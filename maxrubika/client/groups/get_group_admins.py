from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetGroupAdmins:
    async def get_group_admins(
        self: "maxrubika.Messenger",
        group: str,
        show_admin_guids: bool = False,
        all_pages: bool = True,
        start_id: Optional[str] = None
    ):
        """
        Get the list of admins in a group.

        Parameters:
            group (str): The GUID, link, or username of the group.
            show_admin_guids (bool, optional): Show admin GUIDs in output. Default is False.
            all_pages (bool, optional):
                If True, automatically fetch all pages of admins.
                If False, only fetch one page using start_id.
                Default is True.
            start_id (str, optional):
                Starting admin ID for pagination.
                Only used when all_pages is False.

        Returns:
            Data or dict: Result containing all admins with total count.
        """
        from ...data import Data
        from ..exceptions import InvalidInput

        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        if not all_pages:
            input_data = {'group_guid': group_guid}
            if start_id is not None:
                input_data['start_id'] = start_id

            return await self.request(
                method='getGroupAdminMembers',
                input=input_data
            )

        total = 0
        all_admins = []
        admin_guids = set()

        while True:
            input_data = {'group_guid': group_guid}
            if start_id is not None:
                input_data['start_id'] = start_id

            result = await self.request(
                method='getGroupAdminMembers',
                input=input_data
            )

            if isinstance(result, dict):
                result = Data(result)

            admins = result.find_keys('in_chat_members') or []

            if not admins:
                break

            for admin in admins:
                if isinstance(admin, dict):
                    admin = Data(admin)

                join_type = admin.find_keys('join_type')
                if join_type in ('Admin', 'Creator'):
                    admin_guid = admin.find_keys('member_guid')
                    if admin_guid and admin_guid not in admin_guids:
                        admin_guids.add(admin_guid)
                        all_admins.append(admin.to_dict())
                        total += 1

            has_continue = result.find_keys('has_continue')
            if not has_continue:
                break

            next_start_id = result.find_keys('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {
            "admins": all_admins,
            "total": total
        }
        if show_admin_guids:
            result_dict["admin_guids"] = list(admin_guids)

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)