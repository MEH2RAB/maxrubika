from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ChangePassword:
    async def change_password(
        self: "maxrubika.Messenger",
        password: str,
        new_password: str,
        new_hint: str
    ):
        """
        Changes the user's password.

        Parameters:
            password (str): The current password.
            new_password (str): The new password.
            new_hint (str): The new password hint.

        Returns:
            The result of the API call.
        """
        input_data = {
            'password': password,
            'new_password': new_password,
            'new_hint': new_hint
        }

        return await self.request(
            method='changePassword',
            input=input_data
        )