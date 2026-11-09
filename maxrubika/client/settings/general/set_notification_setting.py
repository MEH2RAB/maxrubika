from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

PopupType = Literal['NoPopup', 'OnlyScreenOn', 'OnlyScreenOff', 'Always']
ImportanceType = Literal['Low', 'Medium', 'High', 'Urgent']
VibrateType = Literal['Disabled', 'Default', 'Short', 'Long', 'OnlySilent']

class SetNotificationSetting:
    async def set_notification_setting(
        self: "maxrubika.Messenger",
        user_notification: Optional[bool] = None,
        user_message_preview: Optional[bool] = None,
        group_notification: Optional[bool] = None,
        group_message_preview: Optional[bool] = None,
        channel_notification: Optional[bool] = None,
        channel_message_preview: Optional[bool] = None,
        in_app_sound: Optional[bool] = None,
        in_app_preview: Optional[bool] = None,
        new_contacts: Optional[bool] = None,
        user_notification_popup: Optional[PopupType] = None,
        group_notification_popup: Optional[PopupType] = None,
        channel_notification_popup: Optional[PopupType] = None,
        user_notification_importance: Optional[ImportanceType] = None,
        group_notification_importance: Optional[ImportanceType] = None,
        channel_notification_importance: Optional[ImportanceType] = None,
        user_notification_vibrate: Optional[VibrateType] = None,
        group_notification_vibrate: Optional[VibrateType] = None,
        channel_notification_vibrate: Optional[VibrateType] = None,
        in_app_vibrate: Optional[bool] = None,
        vibrate_voice_calls: Optional[VibrateType] = None
    ):
        """
        Update notification settings.

        Parameters:
            user_notification (bool, optional): Enable/disable user notifications.
            user_message_preview (bool, optional): Show/hide user message preview.
            group_notification (bool, optional): Enable/disable group notifications.
            group_message_preview (bool, optional): Show/hide group message preview.
            channel_notification (bool, optional): Enable/disable channel notifications.
            channel_message_preview (bool, optional): Show/hide channel message preview.
            in_app_sound (bool, optional): Enable/disable in-app sound.
            in_app_preview (bool, optional): Enable/disable in-app preview.
            new_contacts (bool, optional): Enable/disable new contacts notification.
            user_notification_popup (str, optional): 'NoPopup', 'OnlyScreenOn', 'OnlyScreenOff', 'Always'. Case-insensitive.
            group_notification_popup (str, optional): Same as user.
            channel_notification_popup (str, optional): Same as user.
            user_notification_importance (str, optional): 'Low', 'Medium', 'High', 'Urgent'. Case-insensitive.
            group_notification_importance (str, optional): Same as user.
            channel_notification_importance (str, optional): Same as user.
            user_notification_vibrate (str, optional): 'Disabled', 'Default', 'Short', 'Long', 'OnlySilent'. Case-insensitive.
            group_notification_vibrate (str, optional): Same as user.
            channel_notification_vibrate (str, optional): Same as user.
            in_app_vibrate (bool, optional): Enable/disable in-app vibrate.
            vibrate_voice_calls (str, optional): 'Disabled', 'Default', 'Short', 'Long', 'OnlySilent'. Case-insensitive.

        Returns:
            The updated notification settings.
        """
        from ...exceptions import InvalidInput

        settings = {}
        update_parameters = []

        simple_params = {
            'user_notification': user_notification,
            'user_message_preview': user_message_preview,
            'group_notification': group_notification,
            'group_message_preview': group_message_preview,
            'channel_notification': channel_notification,
            'channel_message_preview': channel_message_preview,
            'in_app_sound': in_app_sound,
            'in_app_preview': in_app_preview,
            'new_contacts': new_contacts,
            'in_app_vibrate': in_app_vibrate,
        }
        for key, value in simple_params.items():
            if value is not None:
                settings[key] = value
                update_parameters.append(key)

        enum_params = {
            'user_notification_popup': {'nopopup': 'NoPopup', 'onlyscreenon': 'OnlyScreenOn', 'onlyscreenoff': 'OnlyScreenOff', 'always': 'Always'},
            'group_notification_popup': {'nopopup': 'NoPopup', 'onlyscreenon': 'OnlyScreenOn', 'onlyscreenoff': 'OnlyScreenOff', 'always': 'Always'},
            'channel_notification_popup': {'nopopup': 'NoPopup', 'onlyscreenon': 'OnlyScreenOn', 'onlyscreenoff': 'OnlyScreenOff', 'always': 'Always'},
            'user_notification_importance': {'low': 'Low', 'medium': 'Medium', 'high': 'High', 'urgent': 'Urgent'},
            'group_notification_importance': {'low': 'Low', 'medium': 'Medium', 'high': 'High', 'urgent': 'Urgent'},
            'channel_notification_importance': {'low': 'Low', 'medium': 'Medium', 'high': 'High', 'urgent': 'Urgent'},
            'user_notification_vibrate': {'disabled': 'Disabled', 'default': 'Default', 'short': 'Short', 'long': 'Long', 'onlysilent': 'OnlySilent'},
            'group_notification_vibrate': {'disabled': 'Disabled', 'default': 'Default', 'short': 'Short', 'long': 'Long', 'onlysilent': 'OnlySilent'},
            'channel_notification_vibrate': {'disabled': 'Disabled', 'default': 'Default', 'short': 'Short', 'long': 'Long', 'onlysilent': 'OnlySilent'},
            'vibrate_voice_calls': {'disabled': 'Disabled', 'default': 'Default', 'short': 'Short', 'long': 'Long', 'onlysilent': 'OnlySilent'},
        }

        for key, valid_map in enum_params.items():
            val = locals().get(key)
            if val is not None:
                if isinstance(val, str):
                    normalized = valid_map.get(val.lower())
                    if not normalized:
                        message = f"'{key}' must be one of: {list(valid_map.values())}"
                        raise InvalidInput(message)
                    settings[key] = normalized
                    update_parameters.append(key)
                else:
                    message = f"'{key}' must be a string."
                    raise InvalidInput(message)

        if not settings:
            raise InvalidInput("At least one notification setting must be provided.")

        input_data = {
            'settings': settings,
            'update_parameters': update_parameters
        }

        await self.request(method='setSetting', input=input_data)

        return await self.get_notification_setting()