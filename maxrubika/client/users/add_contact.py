from typing import Union
import re; import maxrubika
from ..exceptions import InvalidInput

class AddContact:
    async def add_contact(
        self: "maxrubika.Client",
        phone_number: Union[str, int],
        first_name: str,
        last_name: str = ''
    ):
        """
        Adds a contact to the client's address book.

        Parameters:
            phone_number (str): The phone number of the contact to be added.
            first_name (str): The first name of the contact.
            last_name (str, optional): The last name of the contact. Defaults to an empty string.

        Returns:
            The result of the API call.

        Note:
            The `phone_number` parameter should be a valid phone number.
            The `first_name` and `last_name` parameters represent the name of the contact.
            If the contact has no last name, `last_name` can be an empty string.
        """
        phone = re.sub(r'[^\d+]', '', phone)

        if phone.startswith('+'):
            phone = phone[1:]

        if phone.startswith('09') and len(phone) == 11:
            phone = '98' + phone[1:]

        if not phone.isdigit():
            raise InvalidInput("Phone number must contain only digits.")

        if len(phone) < 7:
            raise InvalidInput("Phone number is too short (minimum 7 digits).")

        if len(phone) > 15:
            raise InvalidInput("Phone number is too long (maximum 15 digits).")

        input = {
            'phone': phone,
            'first_name': first_name,
            'last_name': last_name
        }
        return await self.request(method = 'addAddressBook', input = input)