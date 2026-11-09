from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ViewCommercial:
    async def view_commercial(
        self: "maxrubika.RubikaTV",
        view_type: Literal["Full", "Half", "Skip"] = "Full"
    ):
        """
        Register a commercial view event.

        Parameters:
            view_type (str): Type of view ("Full", "Half", or "Skip"). Case-insensitive.

        Returns:
            The API output.
        """
        from .exceptions import InvalidInput

        view_type_map = {
            'full': 'Full',
            'half': 'Half',
            'skip': 'Skip'
        }

        normalized_view_type = view_type_map.get(str(view_type).lower())

        if not normalized_view_type:
            message = "'view_type' must be 'Full', 'Half', or 'Skip'."
            raise InvalidInput(message)

        return await self.request(
            method="viewCommercial",
            input={"view_type": normalized_view_type}
        )