import maxrubika
from ...data import Data
from typing import Optional, List, Dict, Any

class GetAllMessages:
    async def get_all_messages(
        self: "maxrubika.Client", 
        chat: str, 
        show_message_ids: bool = False
    ):
        """
        Retrieve all messages from a chat.

        Parameters:
            chat (str): Chat identifier or link (username, GUID, or invite link)
            show_message_ids (bool, optional): Include message IDs in output. Default is False.

        Returns:
            Result containing all messages with total count, first/last IDs, and chat GUID.
        """
        print("Please wait, This may take a while for chats with many messages...\n")

        chat_guid = await self.get_guid(chat)

        mid = "0"
        total = 0
        first_id: Optional[str] = None
        last_id: Optional[str] = None
        all_messages: List[Dict[str, Any]] = []
        message_ids: List[str] = []
        seen_ids: set = set()

        while True:
            result = await self.request(
                method = 'getMessagesInterval',
                input = {'object_guid': chat_guid, 'middle_message_id': mid}
            )

            if not result.messages:
                break

            for msg in result.messages:
                msg_id = msg.message_id
                if msg_id not in seen_ids:
                    seen_ids.add(msg_id)
                    message_ids.append(msg_id)
                    all_messages.append(msg._data)
                    total += 1

            if first_id is None:
                first_id = result.messages[0].message_id
            last_id = result.messages[-1].message_id

            if hasattr(result, 'new_min_id') and result.new_min_id:
                new_mid = str(result.new_min_id)
                if new_mid == mid:
                    break
                mid = new_mid
            else:
                break

            if not hasattr(result, 'new_has_continue') or not result.new_has_continue:
                break

        result_dict = {
            "messages": all_messages,
            "total": total,
            "first_message_id": first_id,
            "last_message_id": last_id,
            "chat_guid": chat_guid
        }
        if show_message_ids:
            result_dict["message_ids"] = message_ids

        return Data(result_dict)