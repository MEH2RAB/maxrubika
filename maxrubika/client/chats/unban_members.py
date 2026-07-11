from typing import List
import maxrubika

class UnbanMembers:
    async def unban_members(
        self: "maxrubika.Client",
        chat: str,
        members: List[str]
    ):
        """
        Unban multiple members from a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of group/channel.
            members (List[str]): List of GUIDs or usernames of members to unban.

        Returns:
            Results of all operations.
        """
        results = []
        for member in members:
            result = await self.unban_member(chat, member)
            results.append(result)
        return result