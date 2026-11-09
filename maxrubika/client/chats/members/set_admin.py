from typing import Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetAdmin:
    GROUP_ALLOWEDS = ["SetAdmin", "BanMember", "ChangeInfo", "PinMessages",
                      "SetJoinLink", "SetMemberAccess", "DeleteGlobalAllMessages"]

    CHANNEL_ALLOWEDS = ["ChangeInfo", "DeleteGlobalAllMessages", "PinMessages",
                        "SetAdmin", "ViewAdmins", "SetJoinLink", "AddMember",
                        "ViewMembers", "SendMessages", "EditAllMessages"]

    GROUP_ACCESS_MAP = {item.lower(): item for item in GROUP_ALLOWEDS}
    CHANNEL_ACCESS_MAP = {item.lower(): item for item in CHANNEL_ALLOWEDS}

    async def set_admin(
        self: "maxrubika.Messenger",
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
            access (Union[List[str], str]): List of allowed permissions or single permission string. Case-insensitive. Can also be 'all' to grant all permissions.
            custom_title (str): Custom title for admin in groups. (optional)

        Returns:
            Result of the operation.
        """
        from ...exceptions import InvalidInput

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

        is_group = chat_guid.startswith('g0')

        if is_group:
            allowed_map = self.GROUP_ACCESS_MAP
            allowed_list = self.GROUP_ALLOWEDS
        else:
            allowed_map = self.CHANNEL_ACCESS_MAP
            allowed_list = self.CHANNEL_ALLOWEDS

        if any(str(item).lower() == 'all' for item in access_list):
            normalized_access = allowed_list.copy()
        else:
            normalized_access = []
            invalid_access = []

            for item in access_list:
                normalized = allowed_map.get(str(item).lower())

                if not normalized:
                    invalid_access.append(item)
                else:
                    normalized_access.append(normalized)

            if invalid_access:
                chat_kind = 'group' if is_group else 'channel'
                message = f'Invalid access for {chat_kind}: {invalid_access}. Allowed: {allowed_list}'
                raise InvalidInput(message)

        if is_group:
            input_data = {
                'group_guid': chat_guid,
                'member_guid': member_guid,
                'action': 'SetAdmin',
                'access_list': normalized_access
            }

            if custom_title:
                input_data['custom_title'] = custom_title

            return await self.request(method='setGroupAdmin', input=input_data)
        else:
            input_data = {
                'channel_guid': chat_guid,
                'member_guid': member_guid,
                'action': 'SetAdmin',
                'access_list': normalized_access
            }

            return await self.request(method='setChannelAdmin', input=input_data)