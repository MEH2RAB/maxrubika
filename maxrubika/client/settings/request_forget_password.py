import maxrubika

class RequestForgetPassword:
    async def request_forget_password(self: "maxrubika.Client"):
        """
        Request to reset the account password.

        Returns:
            The result of the API call.
        """
        return await self.request(method = 'requestForgetPassword')