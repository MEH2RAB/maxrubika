from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UnlockGroup:
    async def unlock_group(
        self: "maxrubika.Messenger",
        group: str
    ):
        """
        Unlock a group by enabling SendMessage access.

        Parameters:
            group (str): The GUID or link of the group.

        Returns:
            Data or dict: Result message.
        """
        from ...data import Data
        from ..exceptions import InvalidInput

        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        access_result = await self.get_group_default_access(group_guid)

        if isinstance(access_result, dict):
            access_result = Data(access_result)

        access_list = access_result.find_keys('access_list')

        if "SendMessages" in access_list:
            result_dict = {
                "status": "OK",
                "message": "Group is already unlocked (SendMessage access enabled)."
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        new_access = access_list + ["SendMessages"]
        await self.set_group_default_access(group_guid, new_access)

        result_dict = {
            "status": "OK",
            "message": "Group unlocked successfully (SendMessage access enabled)."
        }
        if getattr(self, 'as_dict', False):
            return result_dict
        return Data(result_dict)