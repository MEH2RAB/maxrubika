import maxrubika
from typing import Dict, List, Optional

class EditShowLastOnline:
    async def edit_show_last_online(
        self: "maxrubika.Client",
        setting: str,
        exceptions: Optional[Dict[str, List[str]]] = None
    ):
        """
        Edits the setting to control who can see the user's last online status.

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
            show_my_last_online=setting,
            show_my_last_online_exceptions=exceptions
        )