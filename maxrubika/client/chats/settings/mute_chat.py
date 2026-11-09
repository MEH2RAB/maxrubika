from datetime import timedelta
from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class MuteChat:
    async def mute_chat(
        self: "maxrubika.Messenger",
        chat: str,
        duration: Optional[Union[int, timedelta]] = None
    ):
        """
        Mute a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat to mute.
            duration (Union[int, timedelta], optional): Duration of mute. int: seconds, must be at least 1800. timedelta: e.g., timedelta(hours=1). Defaults to None (permanent mute).

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        input_data = {'object_guid': chat_guid, 'action': 'Mute'}

        if duration is not None:
            if isinstance(duration, timedelta):
                duration = int(duration.total_seconds())

            if duration < 1800:
                raise InvalidInput("'duration' must be at least 1800 seconds (30 minutes).")

            input_data['duration'] = duration

        return await self.request(method='setActionChat', input=input_data)