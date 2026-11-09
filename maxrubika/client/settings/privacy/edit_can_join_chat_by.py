from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class EditCanJoinChatBy:
    async def edit_can_join_chat_by(
        self: "maxrubika.Messenger",
        setting: str,
        exceptions: Optional[Dict[str, List[str]]] = None
    ):
        """
        Edits the setting to control who can join your chats by link.

        Parameters:
            setting (str): 'Everybody', 'MyContacts' or 'Nobody'.
            exceptions (Dict[str, List[str]], optional): 'include_users' (always allow) and 'exclude_users' (always deny). Pass {'exclude_users': []} to clear.

        Returns:
            The updated privacy settings after the change.
        """
        return await self.set_privacy_setting(
            can_join_chat_by=setting,
            can_join_chat_by_exceptions=exceptions
        )