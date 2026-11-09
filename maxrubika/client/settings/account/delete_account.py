from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteAccount:
    async def delete_account(self: "maxrubika.Messenger"):
        """
        Request to permanently delete your Rubika account.

        Returns:
            Confirmation message about the deletion request.
        """
        from ....data import Data

        await self.request(method="requestDeleteAccount")

        result_dict = {
            "status": "OK",
            "message": "A confirmation SMS with a deletion link has been sent to your phone.",
            "note": "Creating new accounts after deletion may be restricted."
        }

        if getattr(self, 'as_dict', False):
            return result_dict
        return Data(result_dict)