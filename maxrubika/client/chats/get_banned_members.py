import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class GetBannedMembers:
    async def get_banned_members(
        self: "maxrubika.Client",
        chat: str,
        show_member_guids: bool = False
    ):
        """
        Get a list of banned members in a channel or group.

        Parameters:
            chat (str): The GUID, link, or username of the channel or group.
            show_member_guids (bool, optional): Show member GUIDs in output. Default is False.

        Returns:
            The result containing banned members with total count and optionally GUIDs.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        start_id = None
        total = 0
        all_members = []
        member_guids = set()

        while True:
            if chat_guid.startswith('c0'):
                result = await self.request(
                    method = 'getBannedChannelMembers',
                    input = {'channel_guid': chat_guid, 'start_id': start_id}
                )
            else:
                result = await self.request(
                    method = 'getBannedGroupMembers',
                    input = {'group_guid': chat_guid, 'start_id': start_id}
                )

            if not result or not hasattr(result, 'in_chat_members'):
                break

            for member in result.in_chat_members:
                member_guid = getattr(member, 'member_guid', None)
                if member_guid and member_guid not in member_guids:
                    member_guids.add(member_guid)
                    all_members.append(member.to_dict())
                    total += 1

            if not hasattr(result, 'has_continue') or not result.has_continue:
                break

            if hasattr(result, 'next_start_id') and result.next_start_id:
                start_id = str(result.next_start_id)
            else:
                break

        result_dict = {
            "members": all_members,
            "total": total,
            "chat_guid": chat_guid
        }
        if show_member_guids:
            result_dict["member_guids"] = list(member_guids)

        return Data(result_dict)