from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class FeedbackVoiceTranscription:
    async def feedback_voice_transcription(
        self: "maxrubika.Client",
        chat: Union[str, int],
        message_id: Union[str, int],
        feedback_type: str,
        feedback_text: str = None
    ):
        """
        Send feedback for a voice transcription.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int]): The ID of the voice message.
            feedback_type (str): 'OK' or 'Incorrect'.
            feedback_text (str, optional): Feedback text. If not provided, uses the transcription text.

        Returns:
            The result of the API call.
        """
        if feedback_type not in ('OK', 'Incorrect'):
            raise InvalidInput("feedback_type must be 'OK' or 'Incorrect'.")

        transcription = await self.transcribe_voice(chat, message_id)
        transcription_data = transcription.to_dict() if hasattr(transcription, 'to_dict') else transcription

        transcription_id = transcription_data.get("transcription_id")
        if not transcription_id:
            raise InvalidInput("Failed to get transcription ID.")

        if feedback_text is None:
            feedback_text = transcription_data.get("text", "")

        return await self.request(
            method = 'feedbackTranscription',
            input = {
                'message_id': message_id,
                'transcription_id': transcription_id,
                'feedback_type': feedback_type,
                'feedback_text': feedback_text
            }
        )