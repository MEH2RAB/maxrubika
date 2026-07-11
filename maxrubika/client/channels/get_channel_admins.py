import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class GetChannelAdmins:
    async def get_channel_admins(
        self: "maxrubika.Client",
        channel: str,
        show_admin_guids: bool = False
    ):
        """
        Get the list of admins in a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.
            show_member_guids (bool, optional): Show member GUIDs in output. Default is False.

        Returns:
            Result containing all admins with total count and optionally member_guids.
        """
        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        start_id = None
        total = 0
        all_admins = []
        admin_guids = set()

        while True:
            result = await self.request(
                method = 'getChannelAdminMembers',
                input = {'channel_guid': channel_guid, 'start_id': start_id}
            )

            data = result.to_dict() if hasattr(result, 'to_dict') else result

            if not data or not isinstance(data, dict):
                break

            admins = data.get('in_chat_members', [])
            if not admins:
                break

            for admin in admins:
                join_type = admin.get('join_type', '')
                if join_type in ('Admin', 'Creator'):
                    admin_guid = admin.get('member_guid')
                    if admin_guid and admin_guid not in admin_guids:
                        admin_guids.add(admin_guid)
                        all_admins.append(admin)
                        total += 1

            if not data.get('has_continue', False):
                break

            next_start_id = data.get('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {
            "admins": all_admins,
            "total": total
        }
        if show_admin_guids:
            result_dict["admin_guids"] = list(admin_guids)

        return Data(result_dict)