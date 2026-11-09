from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendFeedback:
    async def send_feedback(
        self: "maxrubika.RubiAI",
        session_id: str,
        message_id: str,
        feedback: Literal["Like", "Dislike", "None"]
    ):
        """
        Submit feedback for an AI message.

        Parameters:
            session_id (str): Identifier of the session containing the message.
            message_id (str): Identifier of the message.
            feedback (str): Feedback value: Like, Dislike, or None. Case-insensitive.

        Returns:
            The API response.
        """
        from .exceptions import InvalidInput

        feedback_map = {
            'like': 'Like',
            'dislike': 'Dislike',
            'none': 'None'
        }

        normalized_feedback = feedback_map.get(str(feedback).lower())

        if not normalized_feedback:
            message = f"Invalid feedback value '{feedback}'. Allowed values are: 'Like', 'Dislike', 'None'."
            raise InvalidInput(message)

        input_data = {
            "session_id": session_id,
            "message_id": message_id,
            "feedback": normalized_feedback
        }

        return await self.request(
            method="sendFeedback",
            input=input_data
        )