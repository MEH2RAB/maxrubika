from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class BanMember:
    async def ban_member(
        self: "maxrubika.Messenger",
        chat: str,
        member: str
    ):
        """
        Ban a member from a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of group/channel.
            member (str): The GUID or username of member to ban.

        Returns:
            Result of the operation.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("c0", "g0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        member_guid = await self.get_guid(member)

        if not member_guid.startswith(("u0", "b0")):
            message = f"'{member}' does not point to a valid member. Expected a user GUID, bot GUID, or username."
            raise InvalidInput(message)

        if chat_guid.startswith('g0'):
            input_data = {
                'group_guid': chat_guid,
                'member_guid': member_guid,
                'action': 'Set'
            }
            return await self.request(method='banGroupMember', input=input_data)
        else:
            input_data = {
                'channel_guid': chat_guid,
                'member_guid': member_guid,
                'action': 'Set'
            }
            return await self.request(method='banChannelMember', input=input_data)