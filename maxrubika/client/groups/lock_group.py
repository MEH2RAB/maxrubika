from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class LockGroup:
    async def lock_group(
        self: "maxrubika.Messenger",
        group: str
    ):
        """
        Lock a group by disabling SendMessage access.

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

        if "SendMessages" not in access_list:
            result_dict = {
                "status": "OK",
                "message": "Group is already locked (SendMessage access disabled)."
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        new_access = [access for access in access_list if access != "SendMessages"]
        await self.set_group_default_access(group_guid, new_access)

        result_dict = {
            "status": "OK",
            "message": "Group locked successfully (SendMessage access disabled)."
        }
        if getattr(self, 'as_dict', False):
            return result_dict
        return Data(result_dict)