from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class MemberIsAdmin:
    async def member_is_admin(
        self: "maxrubika.Messenger",
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
        from ....data import Data
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        admin_guid = await self.get_guid(member)

        if not admin_guid.startswith(("u0", "b0")):
            message = f"'{member}' does not point to a valid member. Expected a user GUID, bot GUID, or username."
            raise InvalidInput(message)

        if chat_guid.startswith('g0'):
            admins = await self.get_group_admins(chat_guid, show_admin_guids=True)
        else:
            admins = await self.get_channel_admins(chat_guid, show_admin_guids=True)

        if isinstance(admins, dict):
            admins = Data(admins)

        admin_guids = admins.find_keys('admin_guids') or []
        return admin_guid in admin_guids