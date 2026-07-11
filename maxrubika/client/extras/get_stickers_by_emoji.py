import maxrubika

class GetStickersByEmoji:
    async def get_stickers_by_emoji(
        self: "maxrubika.Client",
        emoji: str,
        suggest_by: str = 'All'
    ):
        """
        Get stickers by emoji.

        Parameters:
            emoji (str): The emoji character.
            suggest_by (str): The type of suggestion (default is 'All').

        Returns:
            Stickers corresponding to the provided emoji and suggestion type.
        """
        return await self.request(
            method = 'getStickersByEmoji',
            input = {'emoji_character': emoji, 'suggest_by': suggest_by}
        )