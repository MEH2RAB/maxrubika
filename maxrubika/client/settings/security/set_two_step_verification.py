from typing import Union, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetTwoStepVerification:
    async def set_two_step_verification(
        self: "maxrubika.Messenger",
        password: Union[int, str],
        hint: Optional[str] = None,
        recovery_email: Optional[str] = None
    ):
        """
        Set up two-step verification for the user.

        Parameters:
            password (Union[int, str]): The current user password.
            hint (str, optional): A hint to help remember the password.
            recovery_email (str, optional): The recovery email for two-step verification.

        Returns:
            The updated user information after setting up two-step verification.
        """
        input_data = {
            'password': str(password),
            'hint': hint,
            'recovery_email': recovery_email
        }

        return await self.request(method='setupTwoStepVerification', input=input_data)