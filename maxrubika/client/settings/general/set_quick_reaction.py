from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetQuickReaction:
    async def set_quick_reaction(
        self: "maxrubika.Messenger",
        reaction_id: Union[str, int],
        emoji_char: str,
        name: str
    ):
        """
        Set the quick reaction for the current user.

        Parameters:
            reaction_id (str): The reaction ID.
            emoji_char (str): The emoji character (e.g., '👍').
            name (str): The reaction name (e.g., 'Thumbs Up').

        Returns:
            The updated settings.
        """
        input_data = {
            'settings': {
                'quick_reaction': {
                    'reaction_id': reaction_id,
                    'emoji_char': emoji_char,
                    'name': name
                }
            },
            'update_parameters': ['quick_reaction']
        }

        await self.request(
            method='setSetting',
            input=input_data
        )

        return await self.get_device_setting()