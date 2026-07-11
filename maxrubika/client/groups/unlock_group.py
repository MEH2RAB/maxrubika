import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class UnlockGroup:
    async def unlock_group(self: "maxrubika.Client", group: str):
        """
        Unlock a group by enabling SendMessage access.

        Parameters:
            group (str): The GUID or link of the group.

        Returns:
            Result message.
        """
        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        access_result = await self.get_group_default_access(group_guid)
        access_data = access_result.to_dict() if hasattr(access_result, 'to_dict') else access_result
        access_list = access_data.get("access_list", [])

        if "SendMessages" in access_list:
            return Data({"status": "OK", "message": "Group is already unlocked (SendMessage access enabled)."})

        new_access = access_list + ["SendMessages"]
        await self.set_group_default_access(group_guid, new_access)

        return Data({"status": "OK", "message": "Group unlocked successfully (SendMessage access enabled)."})