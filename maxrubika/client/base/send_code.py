from typing import Optional, Literal
import maxrubika
from ..exceptions import InvalidInput

class SendCode:
    async def send_code(
        self: "maxrubika.Client",
        phone_number: str,
        pass_key: Optional[str] = None
    ):
        """
        Send a verification code to a phone number.

        Parameters:
            phone_number (str): The target phone number.
            pass_key (str): The optional account pass key.

        Returns:
            The result of the API call.
        """
        input = {
            'phone_number': phone_number,
            'pass_key': pass_key,
            'send_type': 'SMS'
        }
        return await self.request(
            method = 'sendCode',
            input = input,
            tmp_session = True
        )