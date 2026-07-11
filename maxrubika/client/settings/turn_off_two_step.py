import maxrubika

class TurnOffTwoStep:
    async def turn_off_two_step(self: "maxrubika.Client", password: str):
        """
        Turn off two-step verification passcode for the account.

        Parameters:
            password (str): Current two-step verification password

        Returns:
            Result of the operation.
        """
        return await self.request(method = 'turnOffTwoStep', input = {'password': password})