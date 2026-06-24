from typing import Literal
import maxrubika
from .exceptions import InvalidInput

class UpdateBotEndpoints:
    """
    Register webhook URLs for different event types on Rubika servers.

    This class lets you point Rubika's servers to your own webhook URL
    so events are pushed to you instead of you having to poll for them.
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
            url (str): Full URL that Rubika should call when an event occurs.
                Must be publicly reachable (HTTPS recommended).
            endpoint_type (str): Which kind of event this URL handles. Accepted values:
                - `"ReceiveUpdate"` – new messages, edits, deletions
                - `"ReceiveInlineMessage"` – inline-keyboard button presses
                - `"ReceiveQuery"` – inline-query results
                - `"GetSelectionItem"` – selection menu picks
                - `"SearchSelectionItems"` – search-in-selection requests

        Returns:
            dict: Raw response from the server confirming the registration.
        """
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

        payload = {'url': url, 'type': endpoint_type}

        return await self._request('POST', 'updateBotEndpoints', json = payload)