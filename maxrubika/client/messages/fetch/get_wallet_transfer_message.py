from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetWalletTransferMessage:
    async def get_wallet_transfer_message(
        self: "maxrubika.Messenger",
        transfer_id: str,
        access_transfer: str
    ):
        """
        Get a wallet transfer message details.

        Parameters:
            transfer_id (str): The transfer ID.
            access_transfer (str): The access transfer hash.

        Returns:
            The result of the API call.
        """
        input_data = {
            'transfer_id': transfer_id,
            'access_transfer': access_transfer
        }

        return await self.request(
            method='getWalletTransferMessage',
            input=input_data
        )