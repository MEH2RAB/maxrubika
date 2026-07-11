import maxrubika
from ...data import Data

class GetChats:
    async def get_chats(
        self: "maxrubika.Client",
        show_chat_guids: bool = False
    ):
        """
        Get a list of all chats.

        Parameters:
            show_chat_guids (bool, optional): Show chat GUIDs in output. Default is False.

        Returns:
            Data: The result containing all chats with total count and optionally GUIDs.
        """
        start_id = None
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

            if not hasattr(result, 'has_continue') or not result.has_continue:
                break

            if hasattr(result, 'next_start_id') and result.next_start_id:
                start_id = str(result.next_start_id)
            else:
                break

        result_dict = {
            "chats": all_chats,
            "total": total
        }
        if show_chat_guids:
            result_dict["chat_guids"] = list(chat_guids)

        return Data(result_dict)