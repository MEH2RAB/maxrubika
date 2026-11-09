from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetChatHistory:
    async def get_chat_history(
        self: "maxrubika.RubiAI",
        session_id: str,
        all_pages: bool = True,
        limit: int = 100,
        start_id: Optional[str] = None
    ):
        """
        Retrieve messages from an AI session.

        Parameters:
            session_id (str): Identifier of the session.
            all_pages (bool): Whether to automatically fetch all pages.
            limit (int): Maximum number of messages per request.
            start_id (str, optional): Starting message identifier for pagination.

        Returns:
            The API response.
        """
        from ..data import Data

        if not all_pages:
            input_data = {
                "session_id": session_id,
                "limit": limit,
                "start_id": start_id
            }

            return await self.request(
                method="getChatHistory",
                input=input_data
            )

        all_messages = []
        while True:
            input_data = {
                "session_id": session_id,
                "limit": limit,
                "start_id": start_id
            }

            result = await self.request(
                method="getChatHistory",
                input=input_data
            )

            if isinstance(result, dict):
                result = Data(result)

            if result is None:
                break

            messages = result.find_keys('messages') or []
            all_messages.extend(messages)

            has_continue = result.find_keys('has_continue')
            if has_continue:
                start_id = result.find_keys('next_start_id')
            else:
                break

        result_dict = {"messages": all_messages}

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)