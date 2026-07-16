import maxrubika

class DenyUnconfirmedSession:
    async def deny_unconfirmed_session(
        self: "maxrubika.Client",
        unconfirmed_session_key: str
    ):
        """
        Deny an unconfirmed (pending) session.

        Parameters:
            unconfirmed_session_key (str): The session key to deny.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'actionOnUnconfirmedSession',
            input = {
                'action': 'Deny',
                'unconfirmed_session_key': unconfirmed_session_key
            }
        )