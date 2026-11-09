from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetStringSession:
    async def get_string_session(
        self: "maxrubika.Messenger",
        password: Optional[str] = None
    ) -> str:
        """
        Export current session as an encrypted StringSession.

        Parameters:
            password (str, optional): Optional password for encryption.
                If provided, StringSession can only be opened with this password.

        Returns:
            str: Encrypted StringSession that can be used later with
                 `Messenger(string_session=..., password=...)`.
        """
        from ..core.session import StringSession

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