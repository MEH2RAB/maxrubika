import maxrubika

class CheckTwoStepPasscode:
    async def check_two_step_passcode(self: "maxrubika.Client", password: str):
        """
        Check if the provided two-step verification password is correct.

        Parameters:
            password (str): The two-step verification password to check.

        Returns:
            Result containing status and user data if successful.
        """
        return await self.request(method = 'checkTwoStepPasscode', input = {'password': password})