from typing import Optional, Union, Literal, List, Dict
import re
import maxrubika
from ..exceptions import InvalidInput

PrivacyValue = Literal['Everybody', 'MyContacts', 'Nobody']

class SetSetting:
    async def set_setting(
        self: "maxrubika.Client",
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
        can_called_by_exceptions: Optional[Dict[str, List[str]]] = None,
    ):
        """
        Set various privacy and auto-delete settings for the user.

        Parameters:
            Privacy Settings (accept: 'Everybody', 'MyContacts', 'Nobody'):
                show_my_last_online: Who can see your last online status
                show_my_phone_number: Who can see your phone number
                show_my_profile_photo: Who can see your profile photo
                link_forward_message: Who can forward your message links
                can_join_chat_by: Who can join your chats by link
                show_my_birth_date: Who can see your birth date
                can_called_by: Who can call you

            Exceptions (for privacy settings except link_forward_message):
                Each exception should be a dict with:
                    - 'include_users': List[str] - Users to always allow
                    - 'exclude_users': List[str] - Users to always deny
                    
                To CLEAR exceptions for a setting, pass {'exclude_users': []}:
                    can_called_by_exceptions={'exclude_users': []}

                Example:
                    show_my_last_online_exceptions={
                        'include_users': ['u0abc123...'],
                        'exclude_users': ['u0xyz789...']
                    }

            Auto Delete Messages:
                auto_delete_messages: Message auto-delete duration.

            Delete Inactive Account:
                inactive_account_delete: Delete account after X months.

        Returns:
            The result of the setting operation.
        """
        ALLOWED_PRIVACY = {'Everybody', 'MyContacts', 'Nobody'}

        PRIVACY_WITH_EXCEPTIONS = {
            'show_my_last_online': show_my_last_online,
            'show_my_phone_number': show_my_phone_number,
            'show_my_profile_photo': show_my_profile_photo,
            'can_join_chat_by': can_join_chat_by,
            'show_my_birth_date': show_my_birth_date,
            'can_called_by': can_called_by,
        }

        SETTING_TYPE_MAP = {
            'show_my_last_online': 'ShowLastOnline',
            'show_my_phone_number': 'ShowPhone',
            'show_my_profile_photo': 'ShowPhoto',
            'can_join_chat_by': 'CanJoinChat',
            'show_my_birth_date': 'ShowBirthDate',
            'can_called_by': 'CanCalled',
        }
        input_settings = {}
        update_params = []
        final_exceptions = []

        def add_privacy_setting(key: str, value: Optional[PrivacyValue]):
            if value is not None:
                if value not in ALLOWED_PRIVACY:
                    raise InvalidInput(f'{key} must be one of: {ALLOWED_PRIVACY}')
                input_settings[key] = value
                update_params.append(key)

        for key, value in PRIVACY_WITH_EXCEPTIONS.items():
            add_privacy_setting(key, value)

        exception_params = {
            'show_my_last_online': show_my_last_online_exceptions,
            'show_my_phone_number': show_my_phone_number_exceptions,
            'show_my_profile_photo': show_my_profile_photo_exceptions,
            'can_join_chat_by': can_join_chat_by_exceptions,
            'show_my_birth_date': show_my_birth_date_exceptions,
            'can_called_by': can_called_by_exceptions,
        }

        for setting_key, exceptions in exception_params.items():

            if PRIVACY_WITH_EXCEPTIONS[setting_key] is None:
                if exceptions is not None:
                    raise InvalidInput(
                        f"Cannot set exceptions for '{setting_key}' without setting its privacy level."
                    )
                continue

            if exceptions is None:
                continue

            if not isinstance(exceptions, dict):
                raise InvalidInput(
                    f"'{setting_key}_exceptions' must be a dict or None, got {type(exceptions).__name__}"
                )

            privacy_level = PRIVACY_WITH_EXCEPTIONS[setting_key]
            setting_type = SETTING_TYPE_MAP[setting_key]

            include_users = exceptions.get('include_users', [])
            exclude_users = exceptions.get('exclude_users', [])

            if not isinstance(include_users, list):
                raise InvalidInput(f"'include_users' for '{setting_key}' must be a list.")
            if not isinstance(exclude_users, list):
                raise InvalidInput(f"'exclude_users' for '{setting_key}' must be a list.")

            if privacy_level == 'Everybody':
                if include_users:
                    raise InvalidInput(
                        f"For '{setting_key}' with 'Everybody' level, only 'exclude_users' is allowed."
                    )
            elif privacy_level == 'Nobody':
                if exclude_users:
                    raise InvalidInput(
                        f"For '{setting_key}' with 'Nobody' level, only 'include_users' is allowed."
                    )

            exception = {'setting_type': setting_type}
            if include_users:
                exception['include_users'] = include_users
            if exclude_users:
                exception['exclude_users'] = exclude_users

            final_exceptions.append(exception)
            update_params.append(setting_key)

        if auto_delete_messages is not None:
            auto_delete_value = self._parse_auto_delete(auto_delete_messages)
            input_settings['auto_delete'] = auto_delete_value
            update_params.append('auto_delete')

        if link_forward_message is not None:
            if link_forward_message not in ALLOWED_PRIVACY:
                raise InvalidInput(f'link_forward_message must be one of: {ALLOWED_PRIVACY}')
            input_settings['link_forward_message'] = link_forward_message
            update_params.append('link_forward_message')

        if inactive_account_delete is not None:
            valid_months = {3, 6, 12, 24}
            if inactive_account_delete not in valid_months:
                raise InvalidInput(
                    f"'inactive_account_delete' must be one of: {valid_months}"
                )
            input_settings['delete_account_not_active_months'] = inactive_account_delete
            update_params.append('delete_account_not_active_months')

        if not update_params:
            raise InvalidInput('At least one setting must be provided.')

        if final_exceptions:
            input_settings['exceptions'] = final_exceptions
            if 'exceptions' not in update_params:
                update_params.append('exceptions')

        final_input = {
            'settings': input_settings,
            'update_parameters': update_params
        }

        await self.request(
            method = 'setSetting',
            input = final_input
        )

        return await self.get_privacy_setting()

    def _parse_auto_delete(self, value: Union[str, int]) -> str:
        if isinstance(value, str) and value in ["Off", "1d", "7d", "30d", "1w", "1m", "1y"]:
            return value

        if isinstance(value, int):
            if value == 0:
                return "Off"
            elif 1 <= value <= 365:
                return f"{value}d"
            raise InvalidInput("'auto_delete' days must be between 1 and 365.")

        if isinstance(value, str):
            value = value.lower()
            if value == "off":
                return "Off"

            match = re.match(r'^(\d+)([dwmMy]?)$', value)
            if match:
                num = int(match.group(1))
                unit = match.group(2) or 'd'

                if unit == 'd' and 1 <= num <= 365:
                    return f"{num}d"
                elif unit in ['w', 'W'] and 1 <= num <= 52:
                    return f"{num}w"
                elif unit in ['m', 'M'] and 1 <= num <= 12:
                    return f"{num}m"
                elif unit in ['y', 'Y'] and num == 1:
                    return "1y"

            common_formats = {
                'never': 'Off', 'disabled': 'Off', 'day': '1d',
                'week': '7d', 'month': '30d', 'year': '365d',
            }
            if value in common_formats:
                return common_formats[value]

        raise InvalidInput(
            "'auto_delete' must be: 'Off', days (1-365), "
            "weeks (1w-52w), months (1m-12m), or '1y'"
        )