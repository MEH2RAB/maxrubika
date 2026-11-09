from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetGroupAdminAccess:
    async def get_group_admin_access(
        self: "maxrubika.Messenger",
        group: str,
        admin: str
    ):
        """
        Get the admin access for a member in a group.

        Parameters:
            group (str): The GUID or link of the group.
            admin (str): The GUID or username of the admin for whom admin access is being checked.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        member_guid = await self.get_guid(admin)

        if not member_guid.startswith(("u0", "b0")):
            message = f"'{admin}' does not point to a valid member. Expected a user GUID, bot GUID, or username."
            raise InvalidInput(message)

        input_data = {'group_guid': group_guid, 'member_guid': member_guid}
        return await self.request(
            method='getGroupAdminAccessList',
            input=input_data
        )