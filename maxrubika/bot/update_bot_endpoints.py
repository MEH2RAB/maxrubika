from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UpdateBotEndpoints:
    """
    Register webhook URLs for different event types on Rubika servers.

    This class lets you point Rubika's servers to your own webhook URL so events are pushed to you instead of you having to poll for them.
    """
    async def update_bot_endpoints(
        self: "maxrubika.Bot",
        url: str,
        endpoint_type: Literal[
            "ReceiveUpdate",
            "ReceiveInlineMessage",
            "ReceiveQuery",
            "GetSelectionItem",
            "SearchSelectionItems",
        ] = "ReceiveUpdate",
    ):
        """
        Register a single webhook endpoint on the Rubika server.

        Parameters:
            url (str): Full URL that Rubika should call when an event occurs. Must be publicly reachable (HTTPS recommended).
            endpoint_type (Literal['ReceiveUpdate', 'ReceiveInlineMessage', 'ReceiveQuery', 'GetSelectionItem', 'SearchSelectionItems']): Which kind of event this URL handles. Default is 'ReceiveUpdate'.

        Returns:
            The raw response from the server confirming the registration.
        """
        from ..data import Data
        from .exceptions import InvalidInput, InvalidURL

        allowed_types = [
            'ReceiveUpdate',
            'ReceiveInlineMessage',
            'ReceiveQuery',
            'GetSelectionItem',
            'SearchSelectionItems',
        ]

        if endpoint_type not in allowed_types:
            message = f"Invalid endpoint_type '{endpoint_type}'. Must be one of: {', '.join(allowed_types)}"
            raise InvalidInput(message)

        if not url.startswith(("http://", "https://")):
            raise InvalidInput("url must start with 'http://' or 'https://'")

        input_data = {
            'url': url,
            'type': endpoint_type
        }

        result = await self.request(
            method='updateBotEndpoints',
            input=input_data
        )

        if isinstance(result, dict):
            result = Data(result)

        data = result.find_keys('data')

        inner_status = data.find_keys('status')

        if inner_status == 'InvalidUrl':
            message = "The provided URL is invalid or not properly formatted."
            raise InvalidURL(message)

        return result