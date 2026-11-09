import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendWalletTransferMessage:
    async def send_wallet_transfer_message(
        self: "maxrubika.Messenger",
        chat: str,
        transfer_id: str,
        access_transfer: str
    ):
        """
        Send a wallet transfer message to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            transfer_id (str): The transfer ID.
            access_transfer (str): The access transfer hash.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {
            'object_guid': chat_guid,
            'transfer_id': transfer_id,
            'access_transfer': access_transfer,
            'rnd': random.randint(100000, 999999)
        }

        return await self.request(
            method='sendWalletTransferMessage',
            input=input_data
        )