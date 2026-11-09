from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetChats:
    async def get_chats(
        self: "maxrubika.Messenger",
        show_chat_guids: bool = False,
        all_pages: bool = True,
        start_id: Optional[str] = None
    ):
        """
        Get a list of all chats.

        Parameters:
            show_chat_guids (bool, optional): If True, include chat GUIDs in the result. Default is False.
            all_pages (bool, optional): If True, fetch all pages. If False, only one page using start_id. Default is True.
            start_id (str, optional): Starting chat ID for pagination. Only used when all_pages is False.

        Returns:
            The result of the API call.
        """
        from ....data import Data

        if not all_pages:
            return await self.request(
                method='getChats',
                input={'start_id': start_id}
            )

        total = 0
        all_chats = []
        chat_guids = set()

        while True:
            result = await self.request(
                method='getChats',
                input={'start_id': start_id}
            )

            result_data = Data(result)
            chats = result_data.find_keys('chats') or []

            if not chats:
                break

            for chat in chats:
                chat_data = Data(chat)
                chat_guid = chat_data.find_keys('object_guid')

                if chat_guid and chat_guid not in chat_guids:
                    chat_guids.add(chat_guid)
                    all_chats.append(chat_data.to_dict())
                    total += 1

            has_continue = result_data.find_keys('has_continue')
            if not has_continue:
                break

            next_start_id = result_data.find_keys('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {"chats": all_chats, "total": total}
        if show_chat_guids:
            result_dict["chat_guids"] = list(chat_guids)

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)