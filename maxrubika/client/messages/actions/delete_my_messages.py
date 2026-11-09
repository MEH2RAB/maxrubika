from typing import Union, List, Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteMyMessages:
    async def delete_my_messages(
        self: "maxrubika.Messenger",
        chat: str,
        exclude_message_ids: Optional[Union[str, int, List[Union[str, int]]]] = None,
        type: Literal['Local', 'Global', 'Scheduled'] = 'Global'
    ):
        """
        Delete all messages sent by the authenticated user in a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            exclude_message_ids (Optional[Union[str, int, List[Union[str, int]]]]):
                Message ID(s) to exclude from deletion (preserve them). Default is None.
            type (Literal['Local', 'Global', 'Scheduled']): The type of deletion. Case-insensitive. Default is 'Global'.

        Returns:
            Result of the deletion operation.
        """
        from ....data import Data

        result = await self.get_messages(chat, types="me")

        if isinstance(result, dict):
            result = Data(result)

        messages = result.find_keys('messages') or []

        if not messages:
            result_dict = {
                "status": "OK",
                "message": "No messages found from you in this chat."
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        message_ids = []
        for msg in messages:
            if isinstance(msg, dict):
                msg = Data(msg)
            msg_id = msg.find_keys('message_id')
            if msg_id:
                message_ids.append(str(msg_id))

        if not message_ids:
            result_dict = {
                "status": "OK",
                "message": "No valid message IDs found."
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

        to_delete = [msg_id for msg_id in message_ids if msg_id not in exclude_set]

        if not to_delete:
            result_dict = {
                "status": "OK",
                "message": "All your messages are excluded from deletion.",
                "deleted_count": 0,
                "excluded_count": len(exclude_set),
                "excluded_message_ids": list(exclude_set),
                "total_my_messages": len(message_ids)
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        await self.delete_messages(chat, to_delete, type=type)

        result_dict = {
            "status": "OK",
            "deleted_count": len(to_delete),
            "excluded_count": len(exclude_set),
            "excluded_message_ids": list(exclude_set) if exclude_set else [],
            "total_my_messages": len(message_ids)
        }
        if getattr(self, 'as_dict', False):
            return result_dict
        return Data(result_dict)