from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SearchMovie:
    async def search_movie(
        self: "maxrubika.RubikaTV",
        search_text: str,
        start_id: Optional[str] = None
    ):
        """
        Search for movies by text.

        Parameters:
            search_text (str): Search text.
            start_id (str, optional): Optional starting item ID for pagination.

        Returns:
            The API output.
        """
        input_data = {"search_text": search_text}

        if start_id is not None:
            input_data["start_id"] = start_id

        return await self.request(
            method="search",
            input=input_data
        )