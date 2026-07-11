import maxrubika
from typing import Dict, List, Optional

class EditCanJoinChatBy:
    async def edit_can_join_chat_by(
        self: "maxrubika.Client",
        setting: str,
        exceptions: Optional[Dict[str, List[str]]] = None
    ):
        """
        Edits the setting to control who can join your chats by link.

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
            can_join_chat_by=setting,
            can_join_chat_by_exceptions=exceptions
        )