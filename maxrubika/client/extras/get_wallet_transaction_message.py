import maxrubika

class GetWalletTransactionMessage:
    async def get_wallet_transaction_message(
        self: "maxrubika.Client",
        transfer_id: str,
        access_transfer: str
    ):
        """
        Get the message associated with a wallet transaction.

        Parameters:
            transfer_id (str): The ID of the wallet transaction.
            access_transfer (str): The access hash for the transaction.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'getWalletTransactionMessage',
            input = {
                'transfer_id': transfer_id,
                'access_transfer': access_transfer
            }
        )