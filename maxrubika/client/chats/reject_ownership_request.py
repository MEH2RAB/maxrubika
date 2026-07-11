import maxrubika
from ..exceptions import InvalidInput

class RejectOwnershipRequest:
    async def reject_ownership_request(self: "maxrubika.Client", chat: str):
        """
        Reject an ownership transfer request.

        Parameters:
            chat (str): The GUID, link, or username of the chat (channel/group).

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        return await self.request(
            method = 'replyRequestObjectOwner',
            input = {
                'object_guid': chat_guid,
                'action': 'Reject'
            }
        )