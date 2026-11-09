from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetChannelAdmins:
    async def get_channel_admins(
        self: "maxrubika.Messenger",
        channel: str,
        show_admin_guids: bool = False,
        all_pages: bool = True,
        start_id: Optional[str] = None
    ):
        """
        Get the list of admins in a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.
            show_admin_guids (bool, optional): Show admin GUIDs in output. Default is False.
            all_pages (bool, optional): If True, fetch all pages. If False, only one page using start_id. Default is True.
            start_id (str, optional): Starting admin ID for pagination. Only used when all_pages is False.

        Returns:
            Result containing all admins with total count and optionally admin_guids.
        """
        from ...data import Data
        from ..exceptions import InvalidInput

        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        if not all_pages:
            input_data = {'channel_guid': channel_guid}
            if start_id is not None:
                input_data['start_id'] = start_id

            return await self.request(
                method='getChannelAdminMembers',
                input=input_data
            )

        total = 0
        all_admins = []
        admin_guids = set()

        while True:
            input_data = {'channel_guid': channel_guid}
            if start_id is not None:
                input_data['start_id'] = start_id

            result = await self.request(
                method='getChannelAdminMembers',
                input=input_data
            )

            if isinstance(result, dict):
                result = Data(result)

            admins = result.find_keys('in_chat_members') or []

            if not admins:
                break

            for admin in admins:
                if isinstance(admin, dict):
                    admin = Data(admin)

                join_type = admin.find_keys('join_type')
                if join_type in ('Admin', 'Creator'):
                    admin_guid = admin.find_keys('member_guid')
                    if admin_guid and admin_guid not in admin_guids:
                        admin_guids.add(admin_guid)
                        all_admins.append(admin.to_dict())
                        total += 1

            has_continue = result.find_keys('has_continue')
            if not has_continue:
                break

            next_start_id = result.find_keys('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {
            "admins": all_admins,
            "total": total
        }
        if show_admin_guids:
            result_dict["admin_guids"] = list(admin_guids)

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)