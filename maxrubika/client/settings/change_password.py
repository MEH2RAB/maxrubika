import maxrubika

class ChangePassword:
    async def change_password(
        self: "maxrubika.Client",
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
        return await self.request(
            method = 'changePassword',
            input = {
                'password': password,
                'new_password': new_password,
                'new_hint': new_hint
                }
            )