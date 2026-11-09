from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SignIn:
    async def sign_in(
        self: "maxrubika.Messenger",
        phone_number: str,
        phone_code: str,
        phone_code_hash: str,
        public_key: str
    ):
        """
        Sign in using the verification code.

        Parameters:
            phone_number (str): The phone number.
            phone_code (str): The verification code.
            phone_code_hash (str): The verification code hash.
            public_key (str): The client's public key.

        Returns:
            The result of the API call.
        """
        input_data = {
            'phone_number': phone_number,
            'phone_code': phone_code,
            'phone_code_hash': phone_code_hash,
            'public_key': public_key
        }

        return await self.request(
            method='signIn',
            input=input_data,
            tmp_session=True
        )