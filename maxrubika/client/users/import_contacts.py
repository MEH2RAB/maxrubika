from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ImportContacts:
    async def import_contacts(
        self: "maxrubika.Messenger",
        contacts: List[Dict[str, str]]
    ):
        """
        Import (upload) the phone's contacts to Rubika.

        Parameters:
            contacts (List[Dict[str, str]]): A list of contacts, where each contact is a dict with 'first_name', 'last_name', and 'phone' keys.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method='importAddressBook',
            input={'address_book_items': contacts}
        )