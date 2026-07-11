from typing import Optional, List
import maxrubika

class SetNotification:
    async def set_notification(
        self: "maxrubika.Client",
        user_notification: Optional[bool] = None,
        user_message_preview: Optional[bool] = None,
        group_notification: Optional[bool] = None,
        group_message_preview: Optional[bool] = None,
        channel_notification: Optional[bool] = None,
        channel_message_preview: Optional[bool] = None,
        in_app_sound: Optional[bool] = None,
        in_app_preview: Optional[bool] = None,
        new_contacts: Optional[bool] = None
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

        Returns:
            The updated notification settings.
        """
        settings = {}
        update_parameters = []

        params = {
            'user_notification': user_notification,
            'user_message_preview': user_message_preview,
            'group_notification': group_notification,
            'group_message_preview': group_message_preview,
            'channel_notification': channel_notification,
            'channel_message_preview': channel_message_preview,
            'in_app_sound': in_app_sound,
            'in_app_preview': in_app_preview,
            'new_contacts': new_contacts,
        }

        for key, value in params.items():
            if value is not None:
                settings[key] = value
                update_parameters.append(key)

        if not settings:
            return None

        await self.request(
            method = 'setSetting',
            input = {
                'settings': settings,
                'update_parameters': update_parameters
            }
        )

        return await self.get_notification_setting()