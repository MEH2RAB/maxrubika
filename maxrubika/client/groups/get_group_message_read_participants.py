from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class GetGroupMessageReadParticipants:
    async def get_group_message_read_participants(
        self: "maxrubika.Client",
        group: str,
        message_id: Union[str, int]
    ):
        """
        Get list of participants who have read a specific message in a group.

        Parameters:
            group (str): The GUID or link of the group.
            message_id (Union[str, int]): The ID of the message.

        Returns:
            The result of the API call containing read participants.
        """
        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or link."
            raise InvalidInput(message)

        return await self.request(
            method = 'getGroupMessageReadParticipants',
            input = {
                'group_guid': group_guid,
                'message_id': message_id
            }
        )