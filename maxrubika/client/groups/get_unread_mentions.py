from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class GetUnreadMentions:
    async def get_unread_mentions(
        self: "maxrubika.Client",
        group: str,
        max_id: Union[str, int],
        min_id: Union[str, int],
        sort: str = None
    ):
        """
        Get unread mentions in a group.

        Parameters:
            group (str): The GUID or link of the group.
            max_id (Union[str, int]): Maximum message ID.
            min_id (Union[str, int]): Minimum message ID.
            sort (str, optional): Sort order. Defaults to None.

        Returns:
            The result of the API call containing unread mentions.
        """
        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        input = {
            'object_guid': group_guid,
            'max_id': str(max_id),
            'min_id': str(min_id)
        }

        if sort:
            input['sort'] = sort

        return await self.request(
            method = 'getUnreadMentions',
            input = input
        )