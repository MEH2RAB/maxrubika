from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class RequestRecoveryEmail:
    async def request_recovery_email(
        self: "maxrubika.Messenger",
        password: str,
        recovery_email: str
    ):
        """
        Request a recovery code to be sent to the recovery email.

        Parameters:
            password (str): User's current password.
            recovery_email (str): Recovery email address.

        Returns:
            The result of the API call.
        """
        input_data = {
            "password": password,
            "recovery_email": recovery_email
        }

        return await self.request(method='requestRecoveryEmail', input=input_data)