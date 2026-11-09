from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AbortSetRecoveryEmail:
    async def abort_set_recovery_email(
        self: "maxrubika.Messenger",
        password: str
    ):
        """
        Abort the process of setting a recovery email.

        Parameters:
            password (str): The two-step verification password.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method='abortSetRecoveryEmail',
            input={'password': password}
        )