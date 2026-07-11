import maxrubika
from ..exceptions import InvalidInput

class UnsetAdmin:
    async def unset_admin(
        self: "maxrubika.Client",
        chat: str,
        member: str
    ):
        """
        Unset a member as admin in a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of group/channel.
            member (str): The GUID or username of member to unset as admin.

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

        if chat_guid.startswith('g0'):
            return await self.request(
                method = 'setGroupAdmin',
                input = {
                    'group_guid': chat_guid,
                    'member_guid': member_guid,
                    'action': 'UnsetAdmin',
                    'access_list': []
                    }
                )
        else:
            return await self.request(
                method = 'setChannelAdmin',
                input = {
                    'channel_guid': chat_guid,
                    'member_guid': member_guid,
                    'action': 'UnsetAdmin',
                    'access_list': []
                    }
                )