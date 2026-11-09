from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetGroupMentionList:
    async def get_group_mention_list(
        self: "maxrubika.Messenger",
        group: str,
        search_mention: Optional[str] = None
    ):
        """
        Get the mention list for a group.

        Parameters:
            group (str): The GUID or link of the group.
            search_mention (str, optional): Search text for mentions.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        input_data = {'group_guid': group_guid, 'search_mention': search_mention}
        return await self.request(
            method='getGroupMentionList',
            input=input_data
        )