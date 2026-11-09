from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class EditSession:
    async def edit_session(
        self: "maxrubika.RubiAI",
        session_id: str,
        title: Optional[str] = None,
        is_pinned: Optional[bool] = None
    ):
        """
        Update the pin state and/or title of a session.

        Parameters:
            session_id (str): Identifier of the session.
            title (str, optional): New session title. None means no update.
            is_pinned (bool, optional): New pin state. None means no update.

        Returns:
            The API response.
        """
        input_data = {"session_id": session_id, "update_parameters": []}

        if isinstance(is_pinned, bool):
            input_data["is_pinned"] = is_pinned
            input_data["update_parameters"].append("is_pinned")

        if title:
            input_data["title"] = str(title)
            input_data["update_parameters"].append("title")

        return await self.request(method="editSession", input=input_data)