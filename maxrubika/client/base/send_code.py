from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendCode:
    async def send_code(
        self: "maxrubika.Messenger",
        phone_number: str,
        pass_key: Optional[str] = None
    ):
        """
        Send a verification code to a phone number.

        Parameters:
            phone_number (str): The target phone number.
            pass_key (str, optional): The optional account pass key.

        Returns:
            The result of the API call.
        """
        input_data = {
            'phone_number': phone_number,
            'pass_key': pass_key,
            'send_type': 'SMS'
        }

        return await self.request(
            method='sendCode',
            input=input_data,
            tmp_session=True
        )