from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class EditShowBirthday:
    async def edit_show_birthday(
        self: "maxrubika.Messenger",
        setting: str,
        exceptions: Optional[Dict[str, List[str]]] = None
    ):
        """
        Edits the setting to show or hide the user's birthday.

        Parameters:
            setting (str): 'Everybody', 'MyContacts' or 'Nobody'.
            exceptions (Dict[str, List[str]], optional): 'include_users' (always allow) and 'exclude_users' (always deny). Pass {'exclude_users': []} to clear.

        Returns:
            The updated privacy settings after the change.
        """
        return await self.set_privacy_setting(
            show_my_birth_date=setting,
            show_my_birth_date_exceptions=exceptions
        )