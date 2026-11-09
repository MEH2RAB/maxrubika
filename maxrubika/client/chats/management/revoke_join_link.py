from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class RevokeJoinLink:
    async def revoke_join_link(
        self: "maxrubika.Messenger",
        chat: str,
        join_link: str
    ):
        """
        Revoke an invite link for a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            join_link (str): The join link to revoke.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a group/channel GUID, link, or username."
            raise InvalidInput(message)

        join_link = join_link.split('?')[0].split('#')[0].rstrip('/').split('/')[-1]

        input_data = {
            'object_guid': chat_guid,
            'join_link': join_link
        }

        return await self.request(method='revokeJoinLink', input=input_data)