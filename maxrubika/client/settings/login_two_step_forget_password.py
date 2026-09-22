import maxrubika
from ..base.start import normalize_phone_number

class LoginTwoStepForgetPassword:
    async def login_two_step_forget_password(
        self: "maxrubika.Client",
        phone_number: str
    ):
        """
        Start the password recovery process for two-step verification.

        Use this when the user has forgotten their two-step verification password.
        This will initiate the recovery flow (e.g. sending a code to email/phone).

        Parameters:
            phone_number (str): The phone number associated with the account.

        Returns:
            The result of the API call, typically containing a hash or
            instructions for the next step of recovery.
        """
        phone_number = normalize_phone_number(phone_number)

        return await self.request(
            method = 'loginTwoStepForgetPassword',
            input = {
                'phone_number': phone_number
            }
        )