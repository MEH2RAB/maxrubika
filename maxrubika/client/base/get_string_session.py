from typing import Optional
import maxrubika
from ..core.session import StringSession

class GetStringSession:
    async def get_string_session(
        self: "maxrubika.Client",
        password: Optional[str] = None
    ) -> str:
        """
        Export current session as an encrypted StringSession.

        Parameters:
            password (Optional[str]): Optional password for encryption.
                If provided, StringSession can only be opened with this password.

        Returns:
            str: Encrypted StringSession that can be used later with
                 `Messenger(string_session=..., password=...)`.
        """
        info = self.session.information() if self.session else None

        if info:
            data = {
                "auth": info[1],
                "private_key": info[4]
            }
        else:
            data = {
                "auth": self.auth,
                "private_key": self.private_key
            }
        return str(StringSession.from_data(data, password))