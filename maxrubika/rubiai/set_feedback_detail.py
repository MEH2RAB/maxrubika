from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetFeedbackDetail:
    async def set_feedback_detail(
        self: "maxrubika.RubiAI",
        session_id: str,
        message_id: str,
        feedback_issue_type: str,
        feedback_issue_desc: Optional[str] = None
    ):
        """
        Set detailed information for previously submitted feedback.

        Parameters:
            session_id (str): Identifier of the session.
            message_id (str): Identifier of the message.
            feedback_issue_type (str): Feedback issue/category type (from get_feedback_issues).
            feedback_issue_desc (str, optional): Optional sub-item / description.

        Returns:
            The API response.
        """
        input_data = {
            "session_id": session_id,
            "message_id": message_id,
            "feedback_issue_type": feedback_issue_type,
            "feedback_issue_desc": feedback_issue_desc
        }

        return await self.request(
            method="setFeedbackDetail",
            input=input_data
        )