import maxrubika
from ...data import Data

class GetChats:
    async def get_chats(
        self: "maxrubika.Client",
        show_chat_guids: bool = False,
        auto_start_id: bool = True,
        start_id: str = None
    ):
        """
        Get a list of all chats.

        Parameters:
            show_chat_guids (bool, optional):
                If True, include chat GUIDs in the result.
                Default is False.
            auto_start_id (bool, optional):
                If True, automatically fetch all pages of chats.
                If False, only fetch one page using start_id.
                Default is True.
            start_id (str, optional):
                Starting chat ID for pagination.
                Only used when auto_start_id is False.

        Returns:
            Data: The result containing chats with total count and optionally GUIDs.
        """
        if not auto_start_id:
            return await self.request(
                method = 'getChats',
                input = {'start_id': start_id}
            )
        total = 0
        all_chats = []
        chat_guids = set()

        while True:
            result = await self.request(
                method = 'getChats',
                input = {'start_id': start_id}
            )

            if not result or not hasattr(result, 'chats'):
                break

            for chat in result.chats:
                chat_guid = getattr(chat, 'object_guid', None)
                if chat_guid and chat_guid not in chat_guids:
                    chat_guids.add(chat_guid)
                    all_chats.append(chat.to_dict())
                    total += 1

            if not result.has_continue:
                break

            start_id = str(result.next_start_id) if result.next_start_id else None
            if start_id is None:
                break

        result_dict = {"chats": all_chats, "total": total}
        if show_chat_guids:
            result_dict["chat_guids"] = list(chat_guids)

        return Data(result_dict)