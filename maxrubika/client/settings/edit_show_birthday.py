import maxrubika
from typing import Dict, List, Optional

class EditShowBirthday:
    async def edit_show_birthday(
        self: "maxrubika.Client", 
        setting: str,
        exceptions: Optional[Dict[str, List[str]]] = None
    ):
        """
        Edits the setting to show or hide the user's birthday.

        Parameters:
            setting (str): 'Everybody', 'MyContacts' or 'Nobody'
            exceptions (Optional[Dict[str, List[str]]]): 
                - 'include_users': List[str] - Users to always allow
                - 'exclude_users': List[str] - Users to always deny
                
                To clear exceptions, pass {'exclude_users': []}

        Returns:
            The updated privacy settings after the change.
        """
        return await self.set_setting(
            show_my_birth_date=setting,
            show_my_birth_date_exceptions=exceptions
        )