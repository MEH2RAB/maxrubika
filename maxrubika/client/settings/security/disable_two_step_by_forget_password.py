from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DisableTwoStepByForgetPassword:
    async def disable_two_step_by_forget_password(
        self: "maxrubika.Messenger",
        code: Union[str, int]
    ):
        """
        Disable two-step verification using the recovery code.

        Parameters:
            code (Union[str, int]): The verification code sent to the user.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method='disableTwoStepByForgetPassword',
            input={'code': str(code)}
        )