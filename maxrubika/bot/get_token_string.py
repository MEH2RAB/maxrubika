from typing import Optional
import maxrubika
from .token import TokenString

class GetTokenString:
    async def get_token_string(
        self: "maxrubika.Bot",
        password: Optional[str] = None
    ) -> str:
        """
        Export current bot token as an encrypted TokenString.

        Parameters:
            password (Optional[str]): Optional password for encryption.
                If provided, TokenString can only be opened with this password.

        Returns:
            str: Encrypted TokenString that can be used later with
                 `Bot(token_string=..., password=...)`.
        """
        await self.get_me()

        return str(TokenString.from_token(self.token, password))