from typing import Union, Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class FeedbackVoiceTranscription:
    async def feedback_voice_transcription(
        self: "maxrubika.Messenger",
        chat: Union[str, int],
        message_id: Union[str, int],
        feedback_type: Literal['OK', 'Incorrect'] = 'OK',
        feedback_text: Optional[str] = None
    ):
        """
        Send feedback for a voice transcription.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int]): The ID of the voice message.
            feedback_type (Literal['OK', 'Incorrect']): Feedback type. Case-insensitive. Accepts: 'OK', 'Correct', 'Good' (for OK) and 'Incorrect', 'Bad' (for Incorrect). Default: 'OK'.
            feedback_text (str, optional): Feedback text. If not provided, uses the transcription text.

        Returns:
            The result of the API call.
        """
        from ...data import Data
        from ..exceptions import InvalidInput

        feedback_type_map = {
            'ok': 'OK',
            'correct': 'OK',
            'good': 'OK',
            'incorrect': 'Incorrect',
            'bad': 'Incorrect'
        }
        feedback_type = feedback_type_map.get(feedback_type.lower())

        if not feedback_type:
            message = "'feedback_type' must be 'OK', 'Correct', 'Good' (for OK) or 'Incorrect', 'Bad' (for Incorrect)."
            raise InvalidInput(message)

        transcription = await self.transcribe_voice(chat, message_id)

        if isinstance(transcription, dict):
            transcription = Data(transcription)

        transcription_id = transcription.find_keys('transcription_id')

        if not transcription_id:
            raise InvalidInput("Failed to get transcription ID.")

        if feedback_text is None:
            feedback_text = transcription.find_keys('text') or ""

        input_data = {
            'message_id': message_id,
            'transcription_id': transcription_id,
            'feedback_type': feedback_type,
            'feedback_text': feedback_text
        }

        return await self.request(
            method='feedbackTranscription',
            input=input_data
        )