import maxrubika
from ..exceptions import InvalidInput

class MemberIsAdmin:
    async def member_is_admin(
        self: "maxrubika.Client",
        chat: str,
        member: str
    ) -> bool:
        """
        Checks if a member is an admin in a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the group or channel.
            member (str): The GUID or username of the member.

        Returns:
            bool: True if the user is an admin, False otherwise.
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
            admins = await self.get_group_admins(chat, show_member_guids=True)
        else:
            admins = await self.get_channel_admins(chat, show_member_guids=True)

        return member_guid in admins.member_guids