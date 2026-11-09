from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendChatActivity:
    async def send_chat_activity(
        self: "maxrubika.Messenger",
        chat: str,
        activity: Literal['Typing', 'Recording', 'Uploading'] = 'Typing'
    ):
        """
        Sends a chat activity, such as typing, uploading, or recording.

        Parameters:
            chat (str): The GUID, link, or username of the group/user.
            activity (str): The type of activity. 'Typing', 'Recording', or 'Uploading'. Case-insensitive. Defaults to 'Typing'.

        Returns:
            The result of the API call.

        Raises:
            InvalidInput: If the `activity` argument is not one of "Typing", "Uploading", or "Recording".
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "u0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        activity_map = {
            'typing': 'Typing',
            'recording': 'Recording',
            'uploading': 'Uploading',
        }
        activity = activity_map.get(activity.lower())

        if not activity:
            raise InvalidInput("'activity' argument can only be in 'Typing', 'Uploading', or 'Recording'.")

        input_data = {
            'object_guid': chat_guid,
            'activity': activity
        }

        return await self.request(method='sendChatActivity', input=input_data)