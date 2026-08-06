import random
from typing import List
import maxrubika

class SendRubinoProduct:
    async def send_rubino_product(
        self: "maxrubika.Client",
        chat: str,
        store_id: str,
        product_id: str,
        product_varieties: List[dict]
    ):
        """
        Send a Rubino product to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            store_id (str): The store ID.
            product_id (str): The product ID.
            product_varieties (List[dict]): List of product varieties.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'sendRubinoProduct',
            input = {
            'object_guid': chat_guid,
            'store_id': store_id,
            'product_id': product_id,
            'product_varieties': product_varieties,
            'rnd': random.randint(100000, 999999)
        }
    )