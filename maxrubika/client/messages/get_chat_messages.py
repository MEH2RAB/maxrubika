from typing import Optional, Literal, Union
import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

FILTER_TYPES = {'Voice', 'File', 'Music', 'Gif', 'Media', 'Link'}

class GetChatMessages:
    async def get_chat_messages(
        self: "maxrubika.Client",
        chat: str,
        max_id: Union[str, int] = None,
        sort: Literal['FromMax', 'FromMin'] = 'FromMin',
        filter_type: Optional[Literal['Voice', 'File', 'Music', 'Gif', 'Media', 'Link']] = None,
        limit: int = None
    ):
        """
        Get messages from a chat with filtering and pagination.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            max_id (Union[str, int], optional): Maximum message ID to start from.
            sort (Literal['FromMax', 'FromMin']): Sort direction. Default is 'FromMin'.
            filter_type (Literal, optional): Filter messages by type:
                'Voice', 'File', 'Music', 'Gif', 'Media', 'Link'
            limit (int, optional): Maximum number of messages to retrieve. If None, fetches all messages.

        Returns:
            The result containing messages, count, and pagination info.
        """
        chat_guid = await self.get_guid(chat)

        sort_lower = sort.lower()
        if sort_lower == 'frommax':
            sort = 'FromMax'
        elif sort_lower == 'frommin':
            sort = 'FromMin'
        else:
            raise InvalidInput(f"Invalid sort: '{sort}'. Must be 'FromMax' or 'FromMin'.")

        if filter_type is not None:
            filter_type_lower = filter_type.lower()
            matched = None
            for ft in FILTER_TYPES:
                if ft.lower() == filter_type_lower:
                    matched = ft
                    break
            if matched is None:
                raise InvalidInput(
                    f"Invalid filter_type: '{filter_type}'. Must be one of: {', '.join(sorted(FILTER_TYPES))}"
                )
            filter_type = matched

        current_id = str(max_id) if max_id is not None else None
        all_messages = []
        message_ids = set()

        while True:
            input = {
                'object_guid': chat_guid,
                'sort': sort,
                'limit': 25
            }
            if current_id is not None:
                if sort == 'FromMax':
                    input['max_id'] = current_id
                else:
                    input['min_id'] = current_id

            if filter_type is not None:
                input['filter_type'] = filter_type

            result = await self.request(method='getMessages', input=input)
            data = result.to_dict() if hasattr(result, 'to_dict') else result
            messages = data.get('messages', [])

            if not messages:
                break

            for msg in messages:
                msg_dict = msg.to_dict() if hasattr(msg, 'to_dict') else msg
                msg_id = int(msg_dict.get('message_id', 0))
                
                if msg_id not in message_ids:
                    message_ids.add(msg_id)
                    all_messages.append(msg_dict)

                    if limit is not None and len(all_messages) >= limit:
                        break

            if limit is not None and len(all_messages) >= limit:
                break

            if not data.get('has_continue', True):
                break

            if sort == 'FromMax':
                next_id = data.get('new_max_id')
            else:
                next_id = data.get('new_min_id')

            if not next_id or str(next_id) == current_id:
                break

            current_id = str(next_id)

        result_dict = {
            "messages": all_messages[:limit] if limit else all_messages,
            "count": len(all_messages[:limit]) if limit else len(all_messages),
            "chat_guid": chat_guid
        }

        if all_messages:
            if sort == 'FromMax':
                result_dict["first_message_id"] = str(all_messages[-1].get('message_id', ''))
                result_dict["last_message_id"] = str(all_messages[0].get('message_id', ''))
            else:
                result_dict["first_message_id"] = str(all_messages[0].get('message_id', ''))
                result_dict["last_message_id"] = str(all_messages[-1].get('message_id', ''))

        if filter_type is not None:
            result_dict["filter_type"] = filter_type

        return Data(result_dict)