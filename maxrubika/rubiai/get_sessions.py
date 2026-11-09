from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetSessions:
    async def get_sessions(
        self: "maxrubika.RubiAI",
        all_pages: bool = True,
        limit: int = 10,
        start_id: Optional[str] = None
    ):
        """
        Retrieve AI chat sessions.

        Parameters:
            all_pages (bool): Whether to automatically paginate through all sessions.
            limit (int): Maximum number of sessions requested per API call.
            start_id (str, optional): Starting session ID for pagination. Only used when all_pages is False or as the initial point.

        Returns:
            The API response.
        """
        from ..data import Data

        if not all_pages:
            input_data = {
                "start_id": start_id,
                "limit": limit
            }

            return await self.request(
                method="getSessions",
                input=input_data
            )

        all_sessions = []

        while True:
            input_data = {
                "start_id": start_id,
                "limit": limit
            }

            result = await self.request(
                method="getSessions",
                input=input_data
            )

            if isinstance(result, dict):
                result = Data(result)

            if result is None:
                break

            sessions = result.find_keys('sessions') or []
            all_sessions.extend(sessions)

            has_continue = result.find_keys('has_continue')
            if has_continue:
                start_id = result.find_keys('next_start_id')
            else:
                break

        result_dict = {"sessions": all_sessions}

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)