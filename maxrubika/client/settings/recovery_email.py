import maxrubika

class RecoveryEmail:
    async def recovery_email(
        self: "maxrubika.Client",
        password: str,
        recovery_email: str
    ):
        """
        Recover account using recovery email in two steps.

        Parameters:
            password (str): User's current password
            recovery_email (str): Recovery email address

        Steps:
            1. Requests recovery code to be sent to email
            2. Prompts user for verification code in terminal
            3. Verifies the code
        """
        print("Recovery code sent to email...")
        await self.request(
            method = 'requestRecoveryEmail',
            input = {
                "password": password,
                "recovery_email": recovery_email
            }
        )
        code = input("Enter the code received in email: ").strip()

        result = await self.request(
            method = "verifyRecoveryEmail",
            input = {
                "password": password,
                "code": code
            }
        )
        print("Recovery completed successfully!")
        return result