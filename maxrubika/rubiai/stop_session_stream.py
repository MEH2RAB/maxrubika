from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class StopSessionStream:
    async def stop_session_stream(
        self: "maxrubika.RubiAI",
        session_id: str,
        message_id: str,
        feedback: Literal["Like", "Dislike"] = "Like"
    ):
        """
        Stop an active AI session stream and submit the final feedback.

        Parameters:
            session_id (str): Identifier of the session.
            message_id (str): Identifier of the streamed message.
            feedback (str): Final feedback value. Case-insensitive.
                Accepts: 'Like', 'Dislike' (and 'Good'/'Bad' as aliases).

        Returns:
            The API response.

        Raises:
            InvalidInput: If feedback is invalid.
        """
        from .exceptions import InvalidInput

        feedback_map = {
            'like': 'Like',
            'good': 'Like',
            'dislike': 'Dislike',
            'bad': 'Dislike'
        }

        normalized_feedback = feedback_map.get(str(feedback).lower())

        if not normalized_feedback:
            message = f"Invalid feedback value '{feedback}'. Allowed values are: 'Like', 'Dislike'."
            raise InvalidInput(message)

        input_data = {
            "session_id": session_id,
            "message_id": message_id,
            "feedback": normalized_feedback
        }

        return await self.request(
            method="stopSessionStream",
            input=input_data
        )