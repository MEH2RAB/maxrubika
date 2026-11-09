from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class BanMembers:
    async def ban_members(
        self: "maxrubika.Messenger",
        chat: str,
        members: List[str]
    ):
        """
        Ban multiple members from a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of group/channel.
            members (List[str]): List of GUIDs or usernames of members to ban.

        Returns:
            Result containing total count, success/failed counts, and banned/failed members.
        """
        from ....data import Data

        total = 0
        success = 0
        failed = 0
        banned = []
        failed_members = []

        for member in members:
            total += 1
            try:
                await self.ban_member(chat, member)
                success += 1
                banned.append(member)
            except Exception:
                failed += 1
                failed_members.append(member)

        result_dict = {
            "status": "OK",
            "total": total,
            "success": success,
            "failed": failed,
            "banned": banned,
            "failed_members": failed_members
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)