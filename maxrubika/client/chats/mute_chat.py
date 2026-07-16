from datetime import timedelta
from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class MuteChat:
    async def mute_chat(
        self: "maxrubika.Client",
        chat: str,
        duration: Union[int, timedelta] = None
    ):
        """
        Mute a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat to mute.
            duration (Union[int, timedelta], optional): Duration of mute.
                - int: seconds, must be at least 1800 (30 minutes).
                - timedelta: e.g., timedelta(hours=1), timedelta(minutes=30).
                Defaults to None (permanent mute).

        Returns:
            Result of the operation.
        """
        chat_guid = await self.get_guid(chat)

        input = {'object_guid': chat_guid, 'action': 'Mute'}

        if duration is not None:
            if isinstance(duration, timedelta):
                duration = int(duration.total_seconds())

            if duration < 1800:
                raise InvalidInput("'duration' must be at least 1800 seconds (30 minutes).")

            input['duration'] = duration

        return await self.request(
            method = 'setActionChat',
            input = input
        )