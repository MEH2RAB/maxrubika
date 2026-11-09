from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPropertyTypes:
    async def get_property_types(
        self: "maxrubika.RubikaTV"
    ):
        """
        Retrieve available property types.

        Returns:
            The API output.
        """
        return await self.request(method="getPropertyTypes")