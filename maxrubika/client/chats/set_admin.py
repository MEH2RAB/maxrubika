from typing import Union, List
import maxrubika
from ..exceptions import InvalidInput

class SetAdmin:
    GROUP_ALLOWEDS = ["SetAdmin", "BanMember", "ChangeInfo", "PinMessages", 
                     "SetJoinLink", "SetMemberAccess", "DeleteGlobalAllMessages"]

    CHANNEL_ALLOWEDS = ["ChangeInfo", "DeleteGlobalAllMessages", "PinMessages", 
                       "SetAdmin", "ViewAdmins", "SetJoinLink", "AddMember", 
                       "ViewMembers", "SendMessages", "EditAllMessages"]

    async def set_admin(
        self: "maxrubika.Client",
        chat: str,
        member: str,
        access: Union[List[str], str] = [],
        custom_title: str = ""
    ):
        """
        Set a member as admin in a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of group/channel.
            member (str): The GUID or username of member to set as admin.
            access (Union[List[str], str]): List of allowed permissions or single permission string.
            custom_title (str): Custom title for admin in groups. (optional)

        Returns:
            Result of the operation.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        member_guid = await self.get_guid(member)

        if not member_guid.startswith(("u0", "b0")):
            message = f"'{member}' does not point to a valid member. Expected a user GUID, bot GUID, or username."
            raise InvalidInput(message)

        if isinstance(access, str):
            access_list = [access]
        elif isinstance(access, list):
            access_list = access
        else:
            access_list = []

        if chat_guid.startswith('g0'):
            invalid_access = [item for item in access_list if item not in self.GROUP_ALLOWEDS]
            if invalid_access:
                message = f'Invalid access for group: {invalid_access}. Allowed: {self.GROUP_ALLOWEDS}'
                raise InvalidInput(message)

            input = {
                'group_guid': chat_guid,
                'member_guid': member_guid,
                'action': 'SetAdmin',
                'access_list': access_list
            }
            if custom_title:
                input['custom_title'] = custom_title

            return await self.request(method = 'setGroupAdmin', input = input)

        else:
            invalid_access = [item for item in access_list if item not in self.CHANNEL_ALLOWEDS]
            if invalid_access:
                message = f'Invalid access for channel: {invalid_access}. Allowed: {self.CHANNEL_ALLOWEDS}'
                raise InvalidInput(message)

            return await self.request(
                method = 'setChannelAdmin',
                input = {
                    'channel_guid': chat_guid,
                    'member_guid': member_guid,
                    'action': 'SetAdmin',
                    'access_list': access_list
                }
            )