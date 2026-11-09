from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AbortTwoStepSetup:
    async def abort_two_step_setup(self: "maxrubika.Messenger"):
        """
        Abort the two-step verification setup process.

        Returns:
            The result of the operation.
        """
        return await self.request(method='abortTwoStepSetup')