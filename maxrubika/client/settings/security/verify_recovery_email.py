from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class VerifyRecoveryEmail:
    async def verify_recovery_email(
        self: "maxrubika.Messenger",
        password: str,
        code: Union[str, int]
    ):
        """
        Verify the recovery code sent to the recovery email.

        Parameters:
            password (str): User's current password.
            code (Union[str, int]): The verification code received in email.

        Returns:
            The result of the API call.
        """
        input_data = {
            "password": password,
            "code": code
        }

        return await self.request(method='verifyRecoveryEmail', input=input_data)