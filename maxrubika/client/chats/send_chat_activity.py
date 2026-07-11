from typing import Literal
import maxrubika
from ..exceptions import InvalidInput

class SendChatActivity:
    async def send_chat_activity(
        self: "maxrubika.Client",
        chat: str,
        activity: Literal['Typing', 'Recording', 'Uploading'] = 'Typing'
    ):
        """
        Sends a chat activity, such as typing, uploading, or recording.

        Parameters:
            chat (str): The GUID, link, or username of the group/user.
            activity (str, optional): The type of activity. Defaults to 'Typing'.

        Returns:
            The result of the operation.

        Raises:
            InvalidInput: If the `activity` argument is not one of `"Typing", "Uploading", or "Recording"`.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        if activity not in ('Typing', 'Uploading', 'Recording'):
            message = "'activity' argument can only be in 'Typing', 'Uploading', or 'Recording'."
            raise InvalidInput(message)

        return await self.request(
            method = 'sendChatActivity',
            input = {'object_guid': chat_guid, 'activity': activity})