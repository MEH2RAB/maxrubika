import maxrubika
from ..exceptions import InvalidInput

class RevokeJoinLink:
    async def revoke_join_link(
        self: "maxrubika.Client",
        chat: str,
        join_link: str
    ):
        """
        Revoke a invite link for a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            join_link (str): The join link to revoke.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            raise InvalidInput(
                f"'{chat}' does not point to a valid chat. Expected a group/channel GUID, link, or username."
            )

        join_link = join_link.split("/")[-1]

        return await self.request(
            method = 'revokeJoinLink',
            input = {
                'object_guid': chat_guid,
                'join_link': join_link
            }
        )