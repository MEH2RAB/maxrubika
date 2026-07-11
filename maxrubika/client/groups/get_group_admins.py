import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class GetGroupAdmins:
    async def get_group_admins(
        self: "maxrubika.Client",
        group: str,
        show_admin_guids: bool = False
    ):
        """
        Get the list of admins in a group.

        Parameters:
            group (str): The GUID, link, or username of the group.
            show_admin_guids (bool, optional): Show admin GUIDs in output. Default is False.

        Returns:
            Result containing all admins with total count.
        """
        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        start_id = None
        total = 0
        all_admins = []
        admin_guids = set()

        while True:
            result = await self.request(
                method = 'getGroupAdminMembers',
                input = {'group_guid': group_guid, 'start_id': start_id}
            )

            data = result.to_dict() if hasattr(result, 'to_dict') else result

            if not data or not isinstance(data, dict):
                break

            admins = data.get('in_chat_members', [])
            if not admins:
                break

            for admin in admins:
                join_type = admin.get('join_type', '')
                if join_type in ('Admin', 'Creator'):
                    admin_guid = admin.get('member_guid')
                    if admin_guid and admin_guid not in admin_guids:
                        admin_guids.add(admin_guid)
                        all_admins.append(admin)
                        total += 1

            if not data.get('has_continue', False):
                break

            next_start_id = data.get('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {
            "admins": all_admins,
            "total": total
        }
        if show_admin_guids:
            result_dict["admin_guids"] = list(admin_guids)

        return Data(result_dict)