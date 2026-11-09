from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AddMember:
    async def add_member(
        self: "maxrubika.Messenger",
        chat: str,
        member: str
    ):
        """
        Add a single member to a channel or group.

        Parameters:
            chat (str): The GUID, link, or username of the channel/group.
            member (str): The GUID or username of the member to add.

        Returns:
            The result of the API call.
        """
        return await self.add_members(chat, [member])