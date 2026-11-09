from typing import List, Union, Optional, Literal, TYPE_CHECKING
import re

if TYPE_CHECKING:
    import maxrubika

class GetMessages:
    async def get_messages(
        self: "maxrubika.Messenger",
        chat: str,
        types: Optional[Union[str, List[str]]] = None,
        logic: Literal['OR', 'AND'] = 'OR'
    ):
        """
        Get messages from a chat with optional type filtering.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            types (Union[str, List[str]], optional): Type(s) of messages to filter by. Available types: text, image, video, video_message, voice, music, file, gif, live, location, poll, contact, event, edited, forwarded, sticker, me, bots, users. You can also pass a member GUID or username.
            logic (str): How to combine multiple filters. 'OR' or 'AND'. Case-insensitive. Default is 'OR'.

        Returns:
            - messages: list of filtered messages.
            - count: number of filtered messages.
            - chat_guid: The GUID of the chat.
            - total_all: total messages before filtering.
            - filter_types: list of applied type filters.
            - member_guids: list of applied member GUID filters.
            - logic: the applied logic ('OR' or 'AND').
        """
        from ....data import Data
        from ...exceptions import InvalidInput, InvalidUsername

        VALID_TYPES = {
            "text", "image", "video", "video_message", "voice",
            "music", "file", "gif", "live", "location",
            "poll", "contact", "event", "edited", "forwarded",
            "sticker", "me", "bots", "users"
        }

        MEMBER_GUID_REGEX = r"^(u0)[a-zA-Z0-9]{30}$"

        logic_map = {'or': 'OR', 'and': 'AND'}
        normalized_logic = logic_map.get(str(logic).lower())

        if not normalized_logic:
            raise InvalidInput("'logic' must be 'OR' or 'AND'.")

        if types is None:
            types = []
        elif isinstance(types, str):
            types = [types]

        types = [t.strip() for t in types]

        filter_types = set()
        member_guids = set()
        usernames = []

        for t in types:
            t_lower = t.lower()
            if re.match(MEMBER_GUID_REGEX, t, re.IGNORECASE):
                member_guids.add(t)
            elif t_lower in VALID_TYPES:
                filter_types.add(t_lower)
            else:
                usernames.append(t)

        for username in usernames:
            result = await self.get_info_by_username(username)
            if isinstance(result, dict):
                result = Data(result)
            exist = result.find_keys('exist')
            if not exist:
                message = f"Invalid username: {username}"
                raise InvalidUsername(message)
            obj_type = result.find_keys('type')
            if obj_type == "User":
                member_guids.add(result.find_keys('user_guid'))
            elif obj_type == "Bot":
                member_guids.add(result.find_keys('bot_guid'))
            else:
                message = f"'{username}' is not a user or bot. Cannot filter messages by non-user entities."
                raise InvalidInput(message)

        chat_guid = await self.get_guid(chat)

        if "contact" in filter_types and chat_guid.startswith(("g0", "c0")):
            message = f"Contact messages can only be fetched from private chats (u0/b0), not from '{chat_guid}'"
            raise InvalidInput(message)

        if member_guids and chat_guid.startswith("c0"):
            message = f"Invalid chat_guid '{chat_guid}'. Cannot filter by user messages in channels (c0)."
            raise InvalidInput(message)

        my_guid = None
        if "me" in filter_types:
            my_guid = self.guid

        all_data = await self.get_all_messages(chat_guid)
        if isinstance(all_data, dict):
            all_data = Data(all_data)

        all_messages = all_data.find_keys('messages') or []

        if not filter_types and not member_guids:
            filtered = all_messages
        else:
            filtered = []
            for msg in all_messages:
                match_predicates = self._build_match_predicates(
                    msg=msg,
                    filter_types=filter_types,
                    member_guids=member_guids,
                    my_guid=my_guid
                )

                if not match_predicates:
                    continue

                if normalized_logic == 'OR':
                    matched = any(match_predicates)
                else:
                    matched = all(match_predicates)

                if matched:
                    filtered.append(msg)

        result_dict = {
            "messages": filtered,
            "count": len(filtered),
            "chat_guid": chat_guid,
            "total_all": len(all_messages),
            "filter_types": sorted(filter_types),
            "member_guids": sorted(member_guids),
            "logic": normalized_logic,
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)

    @staticmethod
    def _build_match_predicates(msg, filter_types, member_guids, my_guid):

        msg_type = msg.get("type", "")
        file_inline = msg.get("file_inline", {})
        file_type = file_inline.get("type", "")
        mime = file_inline.get("mime", "").lower()
        is_round = file_inline.get("is_round", False)
        is_edited = msg.get("is_edited", False)
        has_forwarded = "forwarded_from" in msg
        author_guid = msg.get("author_object_guid", "")
        author_type = msg.get("author_type", "")

        predicates = []

        if member_guids:
            predicates.append(author_guid in member_guids)

        if "text" in filter_types:
            predicates.append(msg_type == "Text")

        if "image" in filter_types:
            pred = (
                msg_type == "Image"
                or (
                    msg_type in ("FileInline", "FileInlineCaption")
                    and (
                        mime.startswith("image/")
                        or mime in ("jpg", "jpeg", "png", "gif", "bmp", "webp")
                    )
                )
            )
            predicates.append(pred)

        if "video" in filter_types:
            predicates.append(
                msg_type in ("FileInline", "FileInlineCaption")
                and file_type == "Video"
                and not is_round
            )

        if "video_message" in filter_types:
            predicates.append(
                msg_type in ("FileInline", "FileInlineCaption")
                and file_type == "Video"
                and is_round
            )

        if "voice" in filter_types:
            predicates.append(
                msg_type in ("FileInline", "FileInlineCaption")
                and file_type == "Voice"
            )

        if "music" in filter_types:
            predicates.append(
                msg_type in ("FileInline", "FileInlineCaption")
                and file_type == "Music"
            )

        if "file" in filter_types:
            predicates.append(
                msg_type in ("FileInline", "FileInlineCaption")
                and file_type == "File"
            )

        if "gif" in filter_types:
            predicates.append(
                msg_type in ("FileInline", "FileInlineCaption")
                and file_type == "Gif"
            )

        if "sticker" in filter_types:
            predicates.append(msg_type == "Sticker")

        if "live" in filter_types:
            predicates.append(msg_type == "Live")

        if "location" in filter_types:
            predicates.append(msg_type == "Location")

        if "poll" in filter_types:
            predicates.append(msg_type in ("Poll", "Poll2"))

        if "contact" in filter_types:
            predicates.append(msg_type == "ContactMessage")

        if "event" in filter_types:
            predicates.append(msg_type == "Event")

        if "edited" in filter_types:
            predicates.append(is_edited)

        if "forwarded" in filter_types:
            predicates.append(has_forwarded)

        if "me" in filter_types:
            predicates.append(author_guid == my_guid)

        if "bots" in filter_types:
            predicates.append(author_type == "Bot")

        if "users" in filter_types:
            predicates.append(author_type == "User")

        return predicates