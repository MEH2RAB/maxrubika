from typing import Union
import maxrubika

class VerifyRecoveryEmail:
    async def verify_recovery_email(
        self: "maxrubika.Client",
        password: str,
        code: Union[str, int]
    ):
        """
        Verify the recovery code sent to the recovery email.

        Parameters:
            password (str): User's current password.
            code (Union[str, int]): The verification code received in email.
                Can be a string or an integer.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'verifyRecoveryEmail',
            input = {
                "password": password,
                "code": code
            }
        )