from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class MemberIsOwner:
    async def member_is_owner(
        self: "maxrubika.Messenger",
        chat: str,
        member: str
    ) -> bool:
        """
        Checks if a member is the owner (creator) of a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the group or channel.
            member (str): The GUID or username of the member.

        Returns:
            bool: True if the user is the owner, False otherwise.
        """
        from ....data import Data
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        owner_guid = await self.get_guid(member)

        if not owner_guid.startswith("u0"):
            message = f"'{member}' does not point to a valid member. Expected a user GUID or username."
            raise InvalidInput(message)

        if chat_guid.startswith('g0'):
            admins = await self.get_group_admins(chat_guid)
        else:
            admins = await self.get_channel_admins(chat_guid)

        if isinstance(admins, dict):
            admins = Data(admins)

        admin_list = admins.find_keys('admins') or []

        for admin in admin_list:
            if isinstance(admin, dict):
                admin = Data(admin)

            admin_guid = admin.find_keys('member_guid')
            join_type = admin.find_keys('join_type')

            if admin_guid == owner_guid and join_type == 'Creator':
                return True

        return False