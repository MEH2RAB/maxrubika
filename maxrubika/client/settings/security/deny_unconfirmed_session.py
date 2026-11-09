from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DenyUnconfirmedSession:
    async def deny_unconfirmed_session(
        self: "maxrubika.Messenger",
        unconfirmed_session_key: str
    ):
        """
        Deny an unconfirmed (pending) session.

        Parameters:
            unconfirmed_session_key (str): The session key to deny.

        Returns:
            The result of the API call.
        """
        input_data= {
            'action': 'Deny',
            'unconfirmed_session_key': unconfirmed_session_key
        }

        return await self.request(
            method='actionOnUnconfirmedSession',
            input=input_data
        )