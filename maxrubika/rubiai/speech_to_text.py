import pathlib, io
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SpeechToText:
    async def speech_to_text(
        self: "maxrubika.RubiAI",
        voice_data: Union[str, bytes, "pathlib.Path", "io.BytesIO"]
    ):
        """
        Convert voice data to text using the AI speech-to-text service.

        Parameters:
            voice_data (str | bytes | Path | BytesIO): Audio data as a file path, raw bytes, BytesIO, or a string containing a file path.

        Returns:
            The API response.
        """
        import base64
        import aiofiles
        from .exceptions import InvalidInput

        if isinstance(voice_data, pathlib.Path):
            async with aiofiles.open(voice_data, "rb") as file:
                voice_data = base64.b64encode(await file.read())

        elif isinstance(voice_data, bytes):
            voice_data = base64.b64encode(voice_data)

        elif isinstance(voice_data, io.BytesIO):
            voice_data = base64.b64encode(voice_data.getvalue())

        elif isinstance(voice_data, str):
            path = pathlib.Path(voice_data)
            if path.is_file():
                async with aiofiles.open(path, "rb") as file:
                    voice_data = base64.b64encode(await file.read())
            else:
                message = "'voice_data' must be a valid file path when a string is provided."
                raise InvalidInput(message)

        else:
            message = "'voice_data' must be a pathlib.Path, bytes, io.BytesIO, or a string containing a valid file path."
            raise InvalidInput(message)

        return await self.request(
            method="speechToText",
            input={"voice_data": voice_data.decode()}
        )