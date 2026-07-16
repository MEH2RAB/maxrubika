import maxrubika

class ConfirmUnconfirmedSession:
    async def confirm_unconfirmed_session(
        self: "maxrubika.Client",
        unconfirmed_session_key: str
    ):
        """
        Confirm an unconfirmed (pending) session.

        Parameters:
            unconfirmed_session_key (str): The session key to confirm.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'actionOnUnconfirmedSession',
            input = {
                'action': 'Confirm',
                'unconfirmed_session_key': unconfirmed_session_key
            }
        )