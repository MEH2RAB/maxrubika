from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetGroupMembers:
    async def get_group_members(
        self: "maxrubika.Messenger",
        group: str,
        search_text: Optional[str] = None,
        start_id: Optional[str] = None
    ):
        """
        Get members of a group.

        Parameters:
            group (str): The GUID or link of the group.
            search_text (str, optional): Search text for filtering members. Defaults to None.
            start_id (str, optional): The starting ID for pagination. Defaults to None.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        input_data = {'group_guid': group_guid}

        if search_text:
            input_data['search_text'] = search_text.replace("@", "")

        if start_id:
            input_data['start_id'] = start_id

        return await self.request(method='getGroupAllMembers', input=input_data)