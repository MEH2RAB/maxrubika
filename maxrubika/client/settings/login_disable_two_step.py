import maxrubika
from ..base.start import normalize_phone_number

class LoginDisableTwoStep:
    async def login_disable_two_step(
        self: "maxrubika.Client",
        phone_number: str,
        email_code: str,
        forget_password_code_hash: str
    ):
        """
        Disable two-step verification during login.

        Parameters:
            phone_number (str): The phone number associated with the account.
            email_code (str): The verification code sent to email.
            forget_password_code_hash (str): The code hash for
                forgotten password flow.

        Returns:
            The result of the API call.
        """
        phone_number = normalize_phone_number(phone_number)

        return await self.request(
            method = 'loginDisableTwoStep',
            input = {
                'phone_number': phone_number,
                'email_code': email_code,
                'forget_password_code_hash': forget_password_code_hash
            }
        )