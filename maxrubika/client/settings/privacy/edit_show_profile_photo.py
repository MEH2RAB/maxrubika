from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class EditShowProfilePhoto:
    async def edit_show_profile_photo(
        self: "maxrubika.Messenger",
        setting: str,
        exceptions: Optional[Dict[str, List[str]]] = None
    ):
        """
        Edits the setting to control who can see the user's profile photo.

        Parameters:
            setting (str): 'Everybody', 'MyContacts' or 'Nobody'.
            exceptions (Dict[str, List[str]], optional): 'include_users' (always allow) and 'exclude_users' (always deny). Pass {'exclude_users': []} to clear.

        Returns:
            The updated privacy settings after the change.
        """
        return await self.set_privacy_setting(
            show_my_profile_photo=setting,
            show_my_profile_photo_exceptions=exceptions
        )