from typing import Union
import maxrubika

class SetTwoStepVerification:
    async def set_two_step_verification(
        self: "maxrubika.Client",
        password: Union[int, str],
        hint: str = None,
        recovery_email: str = None
    ):
        """
        Set up two-step verification for the user.

        Parameters:
            password (Union[int, str]): The current user password.
            hint (str): A hint to help remember the password. Defaults to None.
            recovery_email (str): The recovery email for two-step verification. Defaults to None.

        Returns:
            The updated user information after setting up two-step verification.
        """
        return await self.request(
            method = 'setupTwoStepVerification',
            input = {
                'password': str(password),
                'hint': hint,
                'recovery_email': recovery_email
            }
        )