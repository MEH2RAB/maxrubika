from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetFeedbackIssues:
    async def get_feedback_issues(
        self: "maxrubika.RubiAI"
    ):
        """
        Retrieve available feedback issue types.

        Returns:
            Parsed feedback-issues response.
        """
        return await self.request(method="getFeedbackIssues")