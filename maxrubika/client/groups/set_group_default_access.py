from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetGroupDefaultAccess:
    async def set_group_default_access(
        self: "maxrubika.Messenger",
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
                If empty list "[]", ALL access permissions are disabled/closed. Case-insensitive.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

        valid_access_items = {"ViewMembers", "ViewAdmins", "SendMessages", "AddMember"}
        access_map = {item.lower(): item for item in valid_access_items}

        if isinstance(access, str):
            access = [access]

        if not isinstance(access, list):
            message = "Access must be a string or a list of strings."
            raise InvalidInput(message)

        normalized_access = []
        for item in access:
            if not isinstance(item, str):
                message = f"Invalid access item '{item}'. Allowed values: {', '.join(valid_access_items)}"
                raise InvalidInput(message)

            normalized_item = access_map.get(item.lower())
            if not normalized_item:
                message = f"Invalid access item '{item}'. Allowed values: {', '.join(valid_access_items)}"
                raise InvalidInput(message)

            normalized_access.append(normalized_item)

        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        input_data = {'group_guid': group_guid, 'access_list': normalized_access}
        return await self.request(
            method='setGroupDefaultAccess',
            input=input_data
        )