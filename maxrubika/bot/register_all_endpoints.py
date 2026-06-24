from typing import Optional, List
import maxrubika

class RegisterAllEndpoints:
    async def register_all_endpoints(
        self: "maxrubika.Bot",
        base_url: str,
        endpoints: Optional[List[str]] = None
    ):
        """
        Register all webhook endpoints at once.

        This is a convenience method that calls ``update_bot_endpoints``
        for every event type.  Useful during initial setup.

        Parameters:
            base_url (str): Base URL of your server (e.g. `"https://myserver.com"`).
                The path `/wk` will be appended automatically.
            endpoints : list of str, optional
                Which endpoints to register.  If `None`, registers all five.

        Returns:
            list_of_dict: Responses for each registration call.
        """
        if endpoints is None:
            endpoints = [
                'ReceiveUpdate',
                'ReceiveInlineMessage',
                'ReceiveQuery',
                'GetSelectionItem',
                'SearchSelectionItems',
            ]

        base_url = base_url.rstrip("/")
        responses = []

        for etype in endpoints:
            full_url = f"{base_url}/wk"
            resp = await self.update_bot_endpoints(
                url = full_url,
                endpoint_type = etype
            )
            responses.append(resp)

        return responses