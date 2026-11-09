from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMe:
    async def get_me(
        self: "maxrubika.RubikaTV"
    ):
        """
        Retrieve the current VOD account information.

        Returns:
            The API output.
        """
        return await self.request(method="getAccountInfo")