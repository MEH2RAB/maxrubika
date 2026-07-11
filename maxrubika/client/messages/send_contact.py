from typing import Union
import random; import maxrubika
from ..exceptions import InvalidInput

class SendContact:
    async def send_contact(
        self: "maxrubika.Client",
        chat: str,
        phone_number: Union[str, int],
        user: str,
        first_name: str,
        last_name: str = "",
        reply_to_message_id: Union[str, int] = None
    ):
        """
        Send a contact message to a specified chat.

        Parameters:
            chat (str): The GUID or username of the user or bot.
            phone_number (Union[str, int]): Contact's phone number.
            user (str): Contact's username or user GUID.
            first_name (str): Contact's first name.
            last_name (str, optional): Contact's last name. Defaults to "".
            reply_to_message_id (Union[str, int], optional): ID of the message to reply to. Defaults to None.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("b0", "u0")):
            message = f"Contact messages can only be sent in private chats (users or bots), not in '{chat_guid}'"
            raise InvalidInput(message)

        user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        return await self.request(
            method = 'sendMessage',
            input = {
                "message_contact": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone_number": phone_number,
                    "user_guid": user_guid
                },
                "object_guid": chat_guid,
                "rnd": random.randint(100000, 999999),
                "reply_to_message_id": reply_to_message_id
            }
        )