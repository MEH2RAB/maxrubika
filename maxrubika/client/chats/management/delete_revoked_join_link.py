from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteRevokedJoinLink:
    async def delete_revoked_join_link(
        self: "maxrubika.Messenger",
        chat: str,
        join_link: str
    ):
        """
        Delete a specific revoked join link.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            join_link (str): The join link to delete.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid group or channel. Expected a valid GUID, link, or username."
            raise InvalidInput(message)

        join_link_lower = join_link.lower()
        if join_link_lower.startswith(('https://rubika.ir/joing/', 'https://rubika.ir/joinc/')):
            hash_link = join_link.split('?')[0].split('#')[0].rstrip('/').split('/')[-1]
        else:
            message = "'join_link' must start with 'https://rubika.ir/joing/' or 'https://rubika.ir/joinc/'."
            raise InvalidInput(message)

        input_data = {
            'object_guid': chat_guid,
            'join_link': hash_link,
            'type': 'Selected'
        }

        return await self.request(
            method='deleteRevokedJoinLink',
            input=input_data
        )