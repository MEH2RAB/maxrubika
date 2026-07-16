from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class VerifyChangePhoneNumber:
    async def verify_change_phone_number(
        self: "maxrubika.Client",
        code: Union[str, int],
        hash: str
    ):
        """
        Verify phone number change with the received code.

        Parameters:
            code (str): The verification code sent to the new phone number.
            hash (str): The hash received from request_change_phone_number.

        Returns:
            The result of the API call.
        """
        if not code or not code.strip():
            raise InvalidInput("Verification code cannot be empty.")
        if not hash:
            raise InvalidInput("Hash cannot be empty.")

        return await self.request(
            method = 'verifyChangePhoneNumber',
            input = {
                'code': code,
                'hash': hash
            }
        )