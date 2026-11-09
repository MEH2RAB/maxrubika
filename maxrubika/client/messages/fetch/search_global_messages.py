from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SearchGlobalMessages:
    async def search_global_messages(
        self: "maxrubika.Messenger",
        search_text: str,
        all_pages: bool = True,
        start_id: Optional[str] = None,
    ):
        """
        Search for messages globally across all chats.

        Parameters:
            search_text (str): The text or hashtag to search for.
            all_pages (bool, optional):
                If True, automatically fetch all pages of results.
                If False, only fetch one page using start_id.
                Default is True.
            start_id (str, optional): The ID to start fetching from.
                Only used when all_pages is False or as the initial point.

        Returns:
            Result containing messages, total count, and pagination info.
        """
        from ....data import Data

        is_hashtag = search_text.startswith('#')

        if not all_pages:
            input_data = {
                'search_text': search_text[1:] if is_hashtag else search_text,
                'type': 'Hashtag' if is_hashtag else 'Text'
            }
            if start_id is not None:
                input_data['start_id'] = start_id

            return await self.request(
                method='searchGlobalMessages',
                input=input_data
            )

        total = 0
        all_messages = []
        seen_message_ids = set()

        while True:
            input_data = {
                'search_text': search_text[1:] if is_hashtag else search_text,
                'type': 'Hashtag' if is_hashtag else 'Text'
            }
            if start_id is not None:
                input_data['start_id'] = start_id

            result = await self.request(
                method='searchGlobalMessages',
                input=input_data
            )

            if isinstance(result, dict):
                result = Data(result)

            messages = result.find_keys('messages') or []

            if not messages:
                break

            for msg in messages:
                msg_data = Data(msg) if isinstance(msg, dict) else msg
                msg_id = msg_data.find_keys('message_id')

                if msg_id and msg_id not in seen_message_ids:
                    seen_message_ids.add(msg_id)
                    all_messages.append(msg_data.to_dict())
                    total += 1

            has_continue = result.find_keys('has_continue')
            if not has_continue:
                break

            next_start_id = result.find_keys('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {
            "messages": all_messages,
            "total": total
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)