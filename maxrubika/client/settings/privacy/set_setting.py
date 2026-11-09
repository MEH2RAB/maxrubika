from typing import Optional, Union, Literal, List, Dict, TYPE_CHECKING
import warnings

if TYPE_CHECKING:
    import maxrubika

PrivacyValue = Literal['Everybody', 'MyContacts', 'Nobody']

class SetSetting:
    async def set_setting(
        self: "maxrubika.Messenger",
        show_my_last_online: Optional[PrivacyValue] = None,
        show_my_phone_number: Optional[PrivacyValue] = None,
        show_my_profile_photo: Optional[PrivacyValue] = None,
        link_forward_message: Optional[PrivacyValue] = None,
        can_join_chat_by: Optional[PrivacyValue] = None,
        show_my_birth_date: Optional[PrivacyValue] = None,
        can_called_by: Optional[PrivacyValue] = None,
        auto_delete_messages: Optional[Union[str, int]] = None,
        inactive_account_delete: Optional[int] = None,
        show_my_last_online_exceptions: Optional[Dict[str, List[str]]] = None,
        show_my_phone_number_exceptions: Optional[Dict[str, List[str]]] = None,
        show_my_profile_photo_exceptions: Optional[Dict[str, List[str]]] = None,
        can_join_chat_by_exceptions: Optional[Dict[str, List[str]]] = None,
        show_my_birth_date_exceptions: Optional[Dict[str, List[str]]] = None,
        can_called_by_exceptions: Optional[Dict[str, List[str]]] = None
    ):
        """
        Set various privacy and auto-delete settings for the user.

        .. deprecated::
            This method is deprecated and will be removed soon.
            Use `set_privacy_setting` instead.

        Parameters:
            See `set_privacy_setting` for detailed parameter descriptions.

        Returns:
            The updated privacy settings.
        """
        warnings.warn(
            "'set_setting' is deprecated and will be removed soon. Use 'set_privacy_setting' instead.",
            DeprecationWarning,
            stacklevel=2
        )

        return await self.set_privacy_setting(
            show_my_last_online=show_my_last_online,
            show_my_phone_number=show_my_phone_number,
            show_my_profile_photo=show_my_profile_photo,
            link_forward_message=link_forward_message,
            can_join_chat_by=can_join_chat_by,
            show_my_birth_date=show_my_birth_date,
            can_called_by=can_called_by,
            auto_delete_messages=auto_delete_messages,
            inactive_account_delete=inactive_account_delete,
            show_my_last_online_exceptions=show_my_last_online_exceptions,
            show_my_phone_number_exceptions=show_my_phone_number_exceptions,
            show_my_profile_photo_exceptions=show_my_profile_photo_exceptions,
            can_join_chat_by_exceptions=can_join_chat_by_exceptions,
            show_my_birth_date_exceptions=show_my_birth_date_exceptions,
            can_called_by_exceptions=can_called_by_exceptions
        )