import maxrubika

class DeleteAccount:
    async def delete_account(self: "maxrubika.Client"):
        """
        Request to permanently delete your Rubika account.

        Returns:
            str: User-friendly confirmation message.
        """

        print ("A confirmation SMS with an account deletion link has been sent to your phone.\n\n"
            "Note: Due to previous account deletion policies, "
            "there may be restrictions on creating new accounts after deletion.")

        return await self.request(method = "requestDeleteAccount")