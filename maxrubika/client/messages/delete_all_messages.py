from typing import Union, List, Optional
import maxrubika
from ...data import Data

class DeleteAllMessages:
    async def delete_all_messages(
        self: "maxrubika.Client",
        chat: str,
        exclude_message_ids: Optional[Union[str, int, List[Union[str, int]]]] = None
    ):
        """
        Delete all messages in a chat except the first creation event message
        and optionally specified message IDs.

        This method retrieves all messages from the chat and deletes them,
        while preserving:
        - Any message IDs specified in `exclude_message_ids`.

        Parameters:
            chat (str): The GUID, link, or username of the chat
            exclude_message_ids (Union[str, int, List[Union[str, int]]], optional): 
                Message ID(s) to preserve (not delete). Can be string, integer, or list.
                Default is None.

        Returns:
            Result of the deletion operation.
        """
        result = await self.get_all_messages(chat, show_message_ids=True)

        if not result.messages:
            return Data({"status": "OK", "message": "No messages to delete."})

        message_ids = result.message_ids if hasattr(result, 'message_ids') else []

        if not message_ids:
            return Data({"status": "OK", "message": "No messages to delete."})

        exclude_set = set()
        if exclude_message_ids is not None:
            if isinstance(exclude_message_ids, (str, int)):
                exclude_set.add(str(exclude_message_ids))
            elif isinstance(exclude_message_ids, list):
                for item in exclude_message_ids:
                    exclude_set.add(str(item))

        first_message = result.messages[0] if result.messages else None
        preserved_event_id = None

        is_creation_event = (
            first_message and 
            first_message.get('type') == 'Event' and
            first_message.get('event_data', {}).get('type') in ['GroupCreated', 'ChannelCreated']
        )

        if is_creation_event:
            preserved_event_id = first_message.get('message_id')
            if preserved_event_id:
                exclude_set.add(preserved_event_id)

        filtered_ids = [
            msg_id for msg_id in message_ids 
            if msg_id not in exclude_set
        ]

        if not filtered_ids:
            return Data({
                "status": "OK", 
                "message": "All messages are preserved. Nothing to delete.",
                "preserved_count": len(exclude_set)
            })
        await self.delete_messages(chat, filtered_ids)

        return Data({
            "status": "OK",
            "deleted_count": len(filtered_ids),
            "preserved_count": len(exclude_set),
            "preserved_message_ids": list(exclude_set),
            "preserved_event_id": preserved_event_id,
        })