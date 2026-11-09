from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetSessionPlayDuration:
    async def set_session_play_duration(
        self: "maxrubika.RubikaTV",
        session_id: str,
        play_duration: int = 0
    ):
        """
        Set the total play duration for a session.

        Parameters:
            session_id (str): Identifier of the session.
            play_duration (int): Total play duration in seconds.

        Returns:
            The API output.
        """
        input_data = {
            "session_id": session_id,
            "play_duration": play_duration
        }

        return await self.request(
            method="setSessionPlayDuration",
            input=input_data
        )