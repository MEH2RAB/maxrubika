from typing import Optional, Literal, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

NightModeType = Literal['Disable', 'Scheduled', 'Adaptive']
ChatListViewType = Literal['TwoLines', 'ThreeLines']
SwipeGestureType = Literal['ChangeFolder', 'Pin', 'Read', 'Mute', 'Delete']

class SetAppearanceSetting:
    async def set_appearance_setting(
        self: "maxrubika.Messenger",
        large_emoji: Optional[bool] = None,
        android_font_size: Optional[int] = None,
        auto_night_mode: Optional[bool] = None,
        auto_night_mode_type: Optional[NightModeType] = None,
        message_corner: Optional[int] = None,
        chat_list_view: Optional[ChatListViewType] = None,
        chat_list_swipe_gesture: Optional[SwipeGestureType] = None,
        scheduled_use_local_sunset: Optional[bool] = None,
        scheduled_from_time: Optional[Dict[str, int]] = None,
        scheduled_to_time: Optional[Dict[str, int]] = None,
        adaptive_brightness_threshold: Optional[int] = None,
        direct_share: Optional[bool] = None,
        enable_animation: Optional[bool] = None,
        save_to_gallery: Optional[bool] = None,
        send_by_enter: Optional[bool] = None,
        default_tab: Optional[str] = None,
        quick_reaction: Optional[Dict[str, str]] = None
    ):
        """
        Update appearance settings (excluding theme and theme background).

        Parameters:
            large_emoji (bool, optional): Enable/disable large emojis.
            android_font_size (int, optional): Font size for Android.
            auto_night_mode (bool, optional): Enable/disable auto night mode.
            auto_night_mode_type (str, optional): 'Disable', 'Scheduled', 'Adaptive'. Case-insensitive.
            message_corner (int, optional): Message bubble corner radius.
            chat_list_view (str, optional): 'TwoLines' or 'ThreeLines'. Case-insensitive.
            chat_list_swipe_gesture (str, optional): 'ChangeFolder', 'Pin', 'Read', 'Mute', 'Delete'. Case-insensitive.
            scheduled_use_local_sunset (bool, optional): Use local sunset for scheduled night mode.
            scheduled_from_time (Dict[str, int], optional): Scheduled night mode start time (e.g., {'hour': 20, 'minute': 0}).
            scheduled_to_time (Dict[str, int], optional): Scheduled night mode end time (e.g., {'hour': 7, 'minute': 0}).
            adaptive_brightness_threshold (int, optional): Adaptive brightness threshold.
            direct_share (bool, optional): Enable/disable direct share.
            enable_animation (bool, optional): Enable/disable animations.
            save_to_gallery (bool, optional): Enable/disable saving to gallery.
            send_by_enter (bool, optional): Enable/disable sending by Enter key.
            default_tab (str, optional): Default tab.
            quick_reaction (Dict[str, str], optional): Quick reaction with 'reaction_id', 'emoji_char', and 'name'.

        Returns:
            The updated settings.
        """
        from ...exceptions import InvalidInput

        settings = {}
        update_parameters = []

        simple_params = {
            'large_emoji': large_emoji,
            'auto_night_mode': auto_night_mode,
            'scheduled_use_local_sunset': scheduled_use_local_sunset,
            'direct_share': direct_share,
            'enable_animation': enable_animation,
            'save_to_gallery': save_to_gallery,
            'send_by_enter': send_by_enter,
        }
        for key, value in simple_params.items():
            if value is not None:
                settings[key] = value
                update_parameters.append(key)

        int_params = {
            'android_font_size': android_font_size,
            'message_corner': message_corner,
            'adaptive_brightness_threshold': adaptive_brightness_threshold,
        }
        for key, value in int_params.items():
            if value is not None:
                if not isinstance(value, int):
                    message = f"'{key}' must be an integer."
                    raise InvalidInput(message)
                settings[key] = value
                update_parameters.append(key)

        enum_params = {
            'auto_night_mode_type': {
                'disable': 'Disable',
                'scheduled': 'Scheduled',
                'adaptive': 'Adaptive',
            },
            'chat_list_view': {
                'twolines': 'TwoLines',
                'threelines': 'ThreeLines',
            },
            'chat_list_swipe_gesture': {
                'changefolder': 'ChangeFolder',
                'pin': 'Pin',
                'read': 'Read',
                'mute': 'Mute',
                'delete': 'Delete',
            },
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

        time_params = {
            'scheduled_from_time': scheduled_from_time,
            'scheduled_to_time': scheduled_to_time,
        }
        for key, value in time_params.items():
            if value is not None:
                if not isinstance(value, dict) or 'hour' not in value or 'minute' not in value:
                    message = f"'{key}' must be a dict with 'hour' and 'minute'."
                    raise InvalidInput(message)
                settings[key] = value
                update_parameters.append(key)

        if default_tab is not None:
            settings['default_tab'] = default_tab
            update_parameters.append('default_tab')

        if quick_reaction is not None:
            if not isinstance(quick_reaction, dict) or not all(
                k in quick_reaction for k in ('reaction_id', 'emoji_char', 'name')
            ):
                message = "'quick_reaction' must be a dict with 'reaction_id', 'emoji_char', and 'name'."
                raise InvalidInput(message)
            settings['quick_reaction'] = quick_reaction
            update_parameters.append('quick_reaction')

        if not settings:
            raise InvalidInput("At least one appearance setting must be provided.")

        input_data = {
            'settings': settings,
            'update_parameters': update_parameters
        }

        await self.request(method='setSetting', input=input_data)

        return await self.get_device_setting()