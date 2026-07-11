from typing import Union, List, Optional
import maxrubika
from ...data import Data

class DeleteMyMessages:
    async def delete_my_messages(
        self: "maxrubika.Client",
        chat: str,
        exclude_message_ids: Optional[Union[str, int, List[Union[str, int]]]] = None
    ):
        """
        Delete all messages sent by the authenticated user in a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            exclude_message_ids (Optional[Union[str, int, List[Union[str, int]]]]): 
                Message ID(s) to exclude from deletion (preserve them). Default is None.

        Returns:
            Result of the deletion operation.
        """
        result = await self.get_messages(chat, types="me")

        if not result.messages:
            return Data({"status": "OK", "message": "No messages found from you in this chat."})

        message_ids = [str(msg.get("message_id")) for msg in result.messages if msg.get("message_id")]

        if not message_ids:
            return Data({"status": "OK", "message": "No valid message IDs found."})

        exclude_set = set()
        if exclude_message_ids is not None:
            if isinstance(exclude_message_ids, (str, int)):
                exclude_set.add(str(exclude_message_ids))
            elif isinstance(exclude_message_ids, list):
                for item in exclude_message_ids:
                    exclude_set.add(str(item))

        to_delete = [msg_id for msg_id in message_ids if msg_id not in exclude_set]

        if not to_delete:
            return Data({
                "status": "OK",
                "message": "All your messages are excluded from deletion.",
                "deleted_count": 0,
                "excluded_count": len(exclude_set),
                "excluded_message_ids": list(exclude_set)
            })
        await self.delete_messages(chat, to_delete)

        return Data({
            "status": "OK",
            "deleted_count": len(to_delete),
            "excluded_count": len(exclude_set),
            "excluded_message_ids": list(exclude_set) if exclude_set else [],
            "total_my_messages": len(message_ids),
        })