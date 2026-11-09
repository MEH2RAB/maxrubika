from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPendingOwner:
    async def get_pending_owner(self: "maxrubika.Messenger", chat: str):
        """
        Retrieves the pending owner information for a specified chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        return await self.request(
            method='getPendingObjectOwner',
            input={'object_guid': chat_guid}
        )