from typing import Union, List, Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteAllMessages:
    async def delete_all_messages(
        self: "maxrubika.Messenger",
        chat: str,
        exclude_message_ids: Optional[Union[str, int, List[Union[str, int]]]] = None,
        type: Literal['Local', 'Global', 'Scheduled'] = 'Global'
    ):
        """
        Delete all messages in a chat except the first creation event message and optionally specified message IDs.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            exclude_message_ids (Union[str, int, List[Union[str, int]]], optional): Message ID(s) to preserve (not delete). Default is None.
            type (Literal['Local', 'Global', 'Scheduled']): The type of deletion. Case-insensitive. Default is 'Global'.

        Returns:
            Result of the deletion operation.
        """
        from ....data import Data

        result = await self.get_all_messages(chat, show_message_ids=True)

        if isinstance(result, dict):
            result = Data(result)

        messages = result.find_keys('messages') or []

        if not messages:
            result_dict = {
                "status": "OK",
                "message": "No messages to delete."
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        message_ids = result.find_keys('message_ids') or []

        if not message_ids:
            result_dict = {
                "status": "OK",
                "message": "No messages to delete."
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        exclude_set = set()
        if exclude_message_ids is not None:
            if isinstance(exclude_message_ids, (str, int)):
                exclude_set.add(str(exclude_message_ids))
            elif isinstance(exclude_message_ids, list):
                for item in exclude_message_ids:
                    exclude_set.add(str(item))

        first_message = messages[0] if messages else None
        preserved_event_id = None

        if first_message:
            if isinstance(first_message, dict):
                first_message = Data(first_message)

            msg_type = first_message.find_keys('type')
            event_data = first_message.find_keys('event_data')
            if isinstance(event_data, dict):
                event_data = Data(event_data)
            event_type = event_data.find_keys('type') if event_data else None

            is_creation_event = (
                msg_type == 'Event'
                and event_type in ['GroupCreated', 'ChannelCreated']
            )

            if is_creation_event:
                preserved_event_id = first_message.find_keys('message_id')
                if preserved_event_id:
                    exclude_set.add(str(preserved_event_id))

        filtered_ids = [
            msg_id for msg_id in message_ids
            if str(msg_id) not in exclude_set
        ]

        if not filtered_ids:
            result_dict = {
                "status": "OK",
                "message": "All messages are preserved. Nothing to delete.",
                "preserved_count": len(exclude_set)
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        await self.delete_messages(chat, filtered_ids, type=type)

        result_dict = {
            "status": "OK",
            "deleted_count": len(filtered_ids),
            "preserved_count": len(exclude_set),
            "preserved_message_ids": list(exclude_set),
            "preserved_event_id": preserved_event_id,
        }
        if getattr(self, 'as_dict', False):
            return result_dict
        return Data(result_dict)