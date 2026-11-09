from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetAllMessages:
    async def get_all_messages(
        self: "maxrubika.Messenger",
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
        from ....data import Data

        self.logger.info("Please wait, This may take a while for chats with many messages...\n")

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
                method='getMessagesInterval',
                input={'object_guid': chat_guid, 'middle_message_id': mid}
            )

            if isinstance(result, dict):
                result = Data(result)

            messages = result.find_keys('messages') or []

            if not messages:
                break

            for msg in messages:
                msg_data = Data(msg) if isinstance(msg, dict) else msg
                msg_id = msg_data.find_keys('message_id')
                if msg_id and msg_id not in seen_ids:
                    seen_ids.add(msg_id)
                    message_ids.append(str(msg_id))
                    all_messages.append(msg_data.to_dict())
                    total += 1

            if first_id is None and messages:
                first_msg = Data(messages[0]) if isinstance(messages[0], dict) else messages[0]
                first_id = first_msg.find_keys('message_id')
                if first_id is not None:
                    first_id = str(first_id)

            if messages:
                last_msg = Data(messages[-1]) if isinstance(messages[-1], dict) else messages[-1]
                last_id = last_msg.find_keys('message_id')
                if last_id is not None:
                    last_id = str(last_id)

            new_min_id = result.find_keys('new_min_id')
            if new_min_id:
                new_mid = str(new_min_id)
                if new_mid == mid:
                    break
                mid = new_mid
            else:
                break

            new_has_continue = result.find_keys('new_has_continue')
            if not new_has_continue:
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

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)