from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteRevokedJoinLinks:
    async def delete_revoked_join_links(
        self: "maxrubika.Messenger",
        chat: str,
        creator: str
    ):
        """
        Delete all revoked join links created by a specific user.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            creator (str): The creator's GUID or username, or 'me'/'cloud'/'self'/'myself' for the current user.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid group or channel. Expected a valid GUID, link, or username."
            raise InvalidInput(message)

        if creator.lower() in ('me', 'cloud', 'self', 'myself'):
            creator_guid = self.guid
        else:
            creator_guid = await self.get_guid(creator)

        if not creator_guid.startswith("u0"):
            message = f"'{creator}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        input_data = {
            'object_guid': chat_guid,
            'creator_guid': creator_guid,
            'type': 'All'
        }

        return await self.request(
            method='deleteRevokedJoinLink',
            input=input_data
        )