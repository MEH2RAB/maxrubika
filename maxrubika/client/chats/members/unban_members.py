from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UnbanMembers:
    async def unban_members(
        self: "maxrubika.Messenger",
        chat: str,
        members: List[str]
    ):
        """
        Unban multiple members from a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of group/channel.
            members (List[str]): List of GUIDs or usernames of members to unban.

        Returns:
            Data or dict: Result containing total count, success/failed counts, and unbanned/failed members.
        """
        from ....data import Data

        total = 0
        success = 0
        failed = 0
        unbanned = []
        failed_members = []

        for member in members:
            total += 1
            try:
                await self.unban_member(chat, member)
                success += 1
                unbanned.append(member)
            except Exception:
                failed += 1
                failed_members.append(member)

        result_dict = {
            "status": "OK",
            "total": total,
            "success": success,
            "failed": failed,
            "unbanned": unbanned,
            "failed_members": failed_members
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)