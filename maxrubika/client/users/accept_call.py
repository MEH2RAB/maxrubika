from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AcceptCall:
    async def accept_call(
        self: "maxrubika.Messenger",
        call_id: str,
        library_versions: Optional[List[str]] = None,
        max_layer: int = 92,
        min_layer: int = 65
    ):
        """
        Accept an incoming call.

        Parameters:
            call_id (str): The ID of the call to accept.
            library_versions (List[str], optional): List of supported library versions. Default: ['2.7.7', '2.4.4']
            max_layer (int): Maximum protocol layer. Default: 92
            min_layer (int): Minimum protocol layer. Default: 65

        Returns:
            The result of the API call.
        """
        if library_versions is None:
            library_versions = ['2.7.7', '2.4.4']

        input_data = {
            'call_id': call_id,
            'library_versions': library_versions,
            'max_layer': max_layer,
            'min_layer': min_layer
        }

        return await self.request(
            method='acceptCall',
            input=input_data
        )