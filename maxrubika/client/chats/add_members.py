from typing import Union, List
import maxrubika
from ..exceptions import InvalidInput

class AddMembers:
    async def add_members(
        self: "maxrubika.Client",
        chat: str,
        members: Union[str, List[str]]
    ):
        """
        Add members to a channel or group.

        Parameters:
            chat (str): The GUID, link, or username of the channel/group.
            members (Union[str, List[str]]): The GUID(s) or username(s) of the member(s) to be added.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a group or channel GUID, link, or username."
            raise InvalidInput(message)

        if isinstance(members, str):
            members = [members]

        if not members:
            raise InvalidInput("At least one member is required to add to the chat.")

        member_guids = []

        for member in members:
            guid = await self.get_guid(member)

            if not guid.startswith(("u0", "b0")):
                message = f"'{member}' does not point to a valid member. Expected a user GUID, bot GUID, or username."
                raise InvalidInput(message)

            member_guids.append(guid)

        if chat_guid.startswith('c0'):
            return await self.request(
                method = 'addChannelMembers',
                input = {
                    'channel_guid': chat_guid,
                    'member_guids': member_guids
                }
            )
        else:
            return await self.request(
                method = 'addGroupMembers',
                input = {
                    'group_guid': chat_guid,
                    'member_guids': member_guids
                }
            )