from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ConfirmUnconfirmedSession:
    async def confirm_unconfirmed_session(
        self: "maxrubika.Messenger",
        unconfirmed_session_key: str
    ):
        """
        Confirm an unconfirmed (pending) session.

        Parameters:
            unconfirmed_session_key (str): The session key to confirm.

        Returns:
            The result of the API call.
        """
        input_data= {
            'action': 'Confirm',
            'unconfirmed_session_key': unconfirmed_session_key
        }

        return await self.request(
            method='actionOnUnconfirmedSession',
            input=input_data
        )