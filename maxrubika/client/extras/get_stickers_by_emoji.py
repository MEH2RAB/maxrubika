from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetStickersByEmoji:
    async def get_stickers_by_emoji(
        self: "maxrubika.Messenger",
        emoji: str,
        suggest_by: Literal['All', 'MyStickers'] = 'All'
    ):
        """
        Get stickers by emoji.

        Parameters:
            emoji (str): The emoji character.
            suggest_by (Literal['All', 'MyStickers']): The type of suggestion. Case-insensitive. Default is 'All'.

        Returns:
            Stickers corresponding to the provided emoji and suggestion type.
        """
        from ..exceptions import InvalidInput

        suggest_map = {
            'all': 'All',
            'mystickers': 'MyStickers'
        }
        suggest_by = suggest_map.get(suggest_by.lower()) if isinstance(suggest_by, str) else None

        if not suggest_by:
            message = "'suggest_by' must be 'All' or 'MyStickers'."
            raise InvalidInput(message)

        input_data = {'emoji_character': emoji, 'suggest_by': suggest_by}
        return await self.request(
            method='getStickersByEmoji',
            input=input_data
        )