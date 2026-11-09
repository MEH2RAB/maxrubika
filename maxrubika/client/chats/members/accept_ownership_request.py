from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AcceptOwnershipRequest:
    async def accept_ownership_request(
        self: "maxrubika.Messenger",
        chat: str
    ):
        """
        Accept an ownership transfer request.

        Parameters:
            chat (str): The GUID, link, or username of the chat (channel/group).

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        input_data = {
            'object_guid': chat_guid,
            'action': 'Accept'
        }

        return await self.request(method='replyRequestObjectOwner', input=input_data)