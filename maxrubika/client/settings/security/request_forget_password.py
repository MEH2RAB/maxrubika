from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class RequestForgetPassword:
    async def request_forget_password(self: "maxrubika.Messenger"):
        """
        Request to reset the account password.

        Returns:
            The result of the API call.
        """
        return await self.request(method='requestForgetPassword')