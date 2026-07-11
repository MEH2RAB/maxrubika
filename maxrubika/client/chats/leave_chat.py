import maxrubika
from ..exceptions import InvalidInput

class LeaveChat:
    async def leave_chat(self: "maxrubika.Client", chat: str):
        """
        Leave a chat (channel or group).

        Parameters:
            chat (str): The GUID, link, or username of the chat (channel or group).

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        if chat_guid.startswith('c0'):
            return await self.leave_channel(chat_guid)
        else:
            return await self.leave_group(chat_guid)