from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class VerifyChangePhoneNumber:
    async def verify_change_phone_number(
        self: "maxrubika.Messenger",
        code: Union[str, int],
        hash: str
    ):
        """
        Verify phone number change with the received code.

        Parameters:
            code (Union[str, int]): The verification code sent to the new phone number.
            hash (str): The hash received from request_change_phone_number.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        if not code or not str(code).strip():
            raise InvalidInput("Verification code cannot be empty.")
        if not hash:
            raise InvalidInput("Hash cannot be empty.")

        input_data = {
            'code': code,
            'hash': hash
        }

        return await self.request(method='verifyChangePhoneNumber', input=input_data)