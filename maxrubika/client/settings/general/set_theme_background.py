from typing import Literal, Optional, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetThemeBackground:
    async def set_theme_background(
        self: "maxrubika.Messenger",
        theme_id: str,
        type: Literal['System', 'ClientTheme'] = 'ClientTheme',
        chat_background_type: Literal['Color', 'Wallpaper'] = 'Wallpaper',
        wallpaper_id: Optional[str] = None,
        color: Optional[Dict[str, int]] = None
    ):
        """
        Set the background of a theme via setSetting.

        Parameters:
            theme_id (str): Target theme ID.
            type (str): Theme type. 'System' or 'ClientTheme'. Case-insensitive. Default: 'ClientTheme'.
            chat_background_type (str): Background type. 'Color' or 'Wallpaper'. Case-insensitive. Default: 'Wallpaper'.
            wallpaper_id (str, optional): Wallpaper ID (required if chat_background_type='Wallpaper').
            color (dict, optional): RGBA color dict (required if chat_background_type='Color').

        Returns:
            The updated appearance settings after applying the change.
        """
        from ...exceptions import InvalidInput

        type_map = {'system': 'System', 'clienttheme': 'ClientTheme'}
        type = type_map.get(type.lower())
        if not type:
            raise InvalidInput("'type' must be 'System' or 'ClientTheme'.")

        bg_type_map = {'color': 'Color', 'wallpaper': 'Wallpaper'}
        chat_background_type = bg_type_map.get(chat_background_type.lower())
        if not chat_background_type:
            raise InvalidInput("'chat_background_type' must be 'Color' or 'Wallpaper'.")

        if chat_background_type == 'Wallpaper':
            if not wallpaper_id:
                raise InvalidInput("'wallpaper_id' is required for 'Wallpaper'.")
        else:
            if not color:
                raise InvalidInput("'color' is required for 'Color'.")

        theme_bg = {
            'theme_id': theme_id,
            'type': type,
            'chat_background_type': chat_background_type,
            'chat_background_color': color or {'red': 0, 'green': 0, 'blue': 0, 'alpha': 255}
        }
        if wallpaper_id:
            theme_bg['chat_background_wallpaper'] = {'wallpaper_id': wallpaper_id}

        input_data = {
            'settings': {'theme_background': theme_bg},
            'update_parameters': ['theme_background']
        }

        await self.request(method='setSetting', input=input_data)

        return await self.get_appearance_setting()