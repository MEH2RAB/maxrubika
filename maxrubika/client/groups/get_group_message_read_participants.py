from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetGroupMessageReadParticipants:
    async def get_group_message_read_participants(
        self: "maxrubika.Messenger",
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
        from ..exceptions import InvalidInput

        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        input_data = {
            'group_guid': group_guid,
            'message_id': message_id
        }
        return await self.request(
            method='getGroupMessageReadParticipants',
            input=input_data
        )