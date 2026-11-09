from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetTheme:
    async def set_theme(
        self: "maxrubika.Messenger",
        theme_id: str
    ):
        """
        Activate a theme for the current user.

        Parameters:
            theme_id (str): The theme ID to activate.

        Returns:
            The updated appearance settings.
        """
        input_data = {
            'settings': {
                'manual_selected_theme_id': theme_id,
                'auto_day_theme_id': theme_id,
                'auto_dark_theme_id': theme_id
            },
            'update_parameters': [
                'manual_selected_theme_id',
                'auto_day_theme_id',
                'auto_dark_theme_id'
            ]
        }

        await self.request(
            method='setSetting',
            input=input_data
        )

        return await self.get_device_setting()