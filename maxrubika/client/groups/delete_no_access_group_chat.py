from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteNoAccessGroupChat:
    async def delete_no_access_group_chat(
        self: "maxrubika.Messenger",
        group: str
    ):
        """
        Delete (leave) a group chat that the user has no access to.

        Parameters:
            group (str): The GUID or link of the group.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        return await self.request(
            method='deleteNoAccessGroupChat',
            input={'group_guid': group_guid}
        )