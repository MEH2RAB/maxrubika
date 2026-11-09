from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetTwoPasscodeStatus:
    async def get_two_passcode_status(self: "maxrubika.Messenger"):
        """
        Get the two-passcode status for the user.

        Returns:
            The two-passcode status for the user.
        """
        return await self.request(method='getTwoPasscodeStatus')