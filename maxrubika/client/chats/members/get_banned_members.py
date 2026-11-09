from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetBannedMembers:
    async def get_banned_members(
        self: "maxrubika.Messenger",
        chat: str,
        show_member_guids: bool = False,
        all_pages: bool = True,
        start_id: Optional[str] = None
    ):
        """
        Get a list of banned members in a channel or group.

        Parameters:
            chat (str): The GUID, link, or username of the channel or group.
            show_member_guids (bool, optional): Show member GUIDs in output. Default is False.
            all_pages (bool, optional):
                If True, automatically fetch all pages of banned members.
                If False, only fetch one page using start_id.
                Default is True.
            start_id (str, optional):
                Starting member ID for pagination.
                Only used when all_pages is False.

        Returns:
            The result containing banned members with total count and optionally GUIDs.
        """
        from ....data import Data
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        is_channel = chat_guid.startswith("c0")
        method = 'getBannedChannelMembers' if is_channel else 'getBannedGroupMembers'
        guid_key = 'channel_guid' if is_channel else 'group_guid'

        if not all_pages:
            input_data = {guid_key: chat_guid}
            if start_id is not None:
                input_data['start_id'] = start_id

            return await self.request(
                method=method,
                input=input_data
            )

        total = 0
        all_members = []
        member_guids = set()

        while True:
            input_data = {guid_key: chat_guid}
            if start_id is not None:
                input_data['start_id'] = start_id

            result = await self.request(
                method=method,
                input=input_data
            )

            if isinstance(result, dict):
                result = Data(result)

            members = result.find_keys('in_chat_members') or []

            if not members:
                break

            for member in members:
                if isinstance(member, dict):
                    member = Data(member)
                member_guid = member.find_keys('member_guid')
                if member_guid and member_guid not in member_guids:
                    member_guids.add(member_guid)
                    all_members.append(member.to_dict())
                    total += 1

            has_continue = result.find_keys('has_continue')
            if not has_continue:
                break

            next_start_id = result.find_keys('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {
            "members": all_members,
            "total": total,
            "chat_guid": chat_guid
        }
        if show_member_guids:
            result_dict["member_guids"] = list(member_guids)

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)