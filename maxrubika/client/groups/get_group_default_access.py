import maxrubika
from ..exceptions import InvalidInput

class GetGroupDefaultAccess:
    async def get_group_default_access(self: "maxrubika.Client", group: str):
        """
        Get the default access settings for a group.

        Parameters:
            group (str): The GUID or link of the group.

        Returns:
            The result of the API call.
        """
        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        return await self.request(method = 'getGroupDefaultAccess', input = {'group_guid': group_guid})