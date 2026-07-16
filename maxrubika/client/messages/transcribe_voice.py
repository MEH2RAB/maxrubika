from typing import Union
import maxrubika
from ...data import Data

class TranscribeVoice:
    async def transcribe_voice(
        self: "maxrubika.Client",
        chat: Union[str, int],
        message_id: Union[str, int]
    ):
        """
        Transcribes voice messages.

        Parameters:
            chat (str): The GUID, link, or username of the chat (chat, channel, or group) containing the voice message.
            message_id (str): The ID of the voice message.

        Returns:
            The transcription result.
        """
        chat_guid = await self.get_guid(chat)

        transcribe_result = await self.request(
            method = 'transcribeVoice',
            input = {'object_guid': chat_guid, 'message_id': message_id}
        )

        transcribe_data = transcribe_result.to_dict() if hasattr(transcribe_result, 'to_dict') else transcribe_result
        transcription_id = transcribe_data.get("transcription_id")

        if not transcription_id:
            return Data({"status": "ERROR", "message": "Failed to get transcription ID."})

        transcription_result = await self.request(
            method = 'getTranscription',
            input = {'message_id': message_id, 'transcription_id': transcription_id}
        )

        transcription_data = transcription_result.to_dict() if hasattr(transcription_result, 'to_dict') else transcription_result

        return Data({
            "status": transcription_data.get("status", "OK"),
            "text": transcription_data.get("text", ""),
            "transcription_id": transcription_id
        })