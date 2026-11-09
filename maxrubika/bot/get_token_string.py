from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetTokenString:
    async def get_token_string(
        self: "maxrubika.Bot",
        password: Optional[str] = None
    ) -> str:
        """
        Export current bot token as an encrypted TokenString.

        Parameters:
            password (str, optional): Optional password for encryption. If provided, TokenString can only be opened with this password.

        Returns:
            str: Encrypted TokenString that can be used later with `Bot(token_string=..., password=...)`.
        """
        from .token import TokenString

        await self.get_me()

        return str(TokenString.from_token(self.token, password))