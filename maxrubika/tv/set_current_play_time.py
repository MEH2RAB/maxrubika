from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetCurrentPlayTime:
    async def set_current_play_time(
        self: "maxrubika.RubikaTV",
        media_id: str,
        play_time: int
    ):
        """
        Set the current play time for a media.

        Parameters:
            media_id (str): Identifier of the media.
            play_time (int): Current play time in seconds

        Returns:
            The API output.
        """
        from .exceptions import InvalidInput

        if play_time < 0:
            message = "'play_time' must be greater than or equal to 0."
            raise InvalidInput(message)

        input_data = {
            "media_id": media_id,
            "play_time": play_time
        }

        return await self.request(
            method="setCurrentPlayTime",
            input=input_data
        )