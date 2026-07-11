from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class SetGroupDefaultAccess:
    async def set_group_default_access(
        self: "maxrubika.Client",
        group: str,
        access: Union[str, list]
    ):
        """
        Set default access for a group.

        Parameters:
            group (str): The GUID or link of the group.
            access (Union[str, list]): List of allowed actions. Must be one or more of:
                - "ViewMembers": Allows viewing group members.
                - "ViewAdmins": Allows viewing group admins.
                - "SendMessages": Allows sending messages.
                - "AddMember": Allows adding members.
                If only specific actions are listed (e.g. ["SendMessages"]), ONLY those are enabled and others are disabled.
                If empty list "[]", ALL access permissions are disabled/closed.

        Returns:
            The result of the API call.
        """
        valid_access_items = {"ViewMembers", "ViewAdmins", "SendMessages", "AddMember"}

        if isinstance(access, str):
            access = [access]

        if not isinstance(access, list):
            raise InvalidInput("Access must be a string or a list of strings.")

        for item in access:
            if item not in valid_access_items:
                message = f"Invalid access item '{item}'. Allowed values: {', '.join(valid_access_items)}"
                raise InvalidInput(message)

        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        return await self.request(
            method = 'setGroupDefaultAccess',
            input = {'group_guid': group_guid, 'access_list': access}
        )