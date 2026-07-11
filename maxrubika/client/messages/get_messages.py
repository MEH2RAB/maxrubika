from typing import List, Union, Optional
import json; import re; import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class GetMessages:
    async def get_messages(
        self: "maxrubika.Client",
        chat: str,
        types: Optional[Union[str, List[str]]] = None
    ):
        """
        Get messages from a chat with optional type filtering.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            types (Optional[Union[str, List[str]]]): Type(s) of messages to filter by.
                Each item is independent.
                Available types:
                    - "text": Text messages
                    - "image": Image messages
                    - "video": Video messages (non-round)
                    - "video_message": Round video messages
                    - "voice": Voice messages
                    - "music": Music messages
                    - "file": File messages
                    - "gif": GIF messages
                    - "live": Live messages
                    - "location": Location messages
                    - "poll": Poll messages
                    - "contact": Contact messages (only private chats)
                    - "event": Event messages
                    - "edited": Edited messages
                    - "forwarded": Forwarded messages
                    - "sticker": Sticker messages
                    - "me": Messages sent by the client itself
                    - "bots": Messages sent by bots
                    - "users": Messages sent by users
                You can also pass a member GUID or username for member filtering.
                If None, returns all messages.

        Returns:
            - messages: list of filtered messages.
            - count: number of filtered messages.
            - chat_guid: The GUID of the chat.
            - total_all: total messages before filtering.
            - filter_types: list of applied type filters.
            - member_guids: list of applied member GUID filters.
        """
        VALID_TYPES = {
            "text", "image", "video", "video_message", "voice", 
            "music", "file", "gif", "live", "location", 
            "poll", "contact", "event", "edited", "forwarded", 
            "sticker", "me", "bots", "users"
        }

        MEMBER_GUID_REGEX = r"^(u0)[a-zA-Z0-9]{30}$"

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
            if re.match(MEMBER_GUID_REGEX, t):
                member_guids.add(t)
            elif t_lower in VALID_TYPES:
                filter_types.add(t_lower)
            else:
                usernames.append(t)

        for username in usernames:
            result = await self.get_info_by_username(username)
            info = result if isinstance(result, dict) else json.loads(str(result))
            if not info.get("exist"):
                raise ValueError(f"Invalid username: {username}")
            obj_type = info.get("type")
            if obj_type == "User":
                member_guids.add(info["user"]["user_guid"])
            elif obj_type == "Bot":
                member_guids.add(info["bot"]["bot_guid"])
            else:
                raise InvalidInput(
                    f"'{username}' is not a user or bot. Cannot filter messages by non-user entities.")

        chat_guid = await self.get_guid(chat)

        if "contact" in filter_types and chat_guid.startswith(("g0", "c0")):
            raise InvalidInput(
                f"Contact messages can only be fetched from private chats (u0/b0), "
                f"not from '{chat_guid}'"
            )

        if member_guids and chat_guid.startswith("c0"):
            raise InvalidInput(
                f"Invalid chat_guid '{chat_guid}'. "
                "Cannot filter by user messages in channels (c0)."
            )

        my_guid = None
        if "me" in filter_types:
            my_guid = self.guid

        all_data = await self.get_all_messages(chat_guid)
        all_messages = all_data["messages"]

        if not filter_types and not member_guids:
            filtered = all_messages
        else:
            filtered = []
            for msg in all_messages:
                msg_type = msg.get("type", "")
                file_inline = msg.get("file_inline", {})
                file_type = file_inline.get("type", "")
                mime = file_inline.get("mime", "").lower()
                is_round = file_inline.get("is_round", False)
                is_edited = msg.get("is_edited", False)
                has_forwarded = "forwarded_from" in msg
                author_guid = msg.get("author_object_guid", "")
                author_type = msg.get("author_type", "")

                matched = False
                if author_guid in member_guids:
                    matched = True

                if not matched and "text" in filter_types and msg_type == "Text":
                    matched = True

                if not matched and "image" in filter_types:
                    if msg_type == "Image":
                        matched = True
                    elif msg_type in ("FileInline", "FileInlineCaption") and (
                        mime.startswith("image/") or mime in ("jpg", "jpeg", "png", "gif", "bmp", "webp")
                    ):
                        matched = True

                if not matched and "video" in filter_types:
                    if msg_type in ("FileInline", "FileInlineCaption") and file_type == "Video" and not is_round:
                        matched = True

                if not matched and "video_message" in filter_types:
                    if msg_type in ("FileInline", "FileInlineCaption") and file_type == "Video" and is_round:
                        matched = True

                if not matched and "voice" in filter_types:
                    if msg_type in ("FileInline", "FileInlineCaption") and file_type == "Voice":
                        matched = True

                if not matched and "music" in filter_types:
                    if msg_type in ("FileInline", "FileInlineCaption") and file_type == "Music":
                        matched = True

                if not matched and "file" in filter_types:
                    if msg_type in ("FileInline", "FileInlineCaption") and file_type == "File":
                        matched = True

                if not matched and "gif" in filter_types:
                    if msg_type in ("FileInline", "FileInlineCaption") and file_type == "Gif":
                        matched = True

                if not matched and "sticker" in filter_types:
                    if msg_type == "Sticker":
                        matched = True

                if not matched and "live" in filter_types:
                    if msg_type == "Live":
                        matched = True

                if not matched and "location" in filter_types:
                    if msg_type == "Location":
                        matched = True

                if not matched and "poll" in filter_types:
                    if msg_type in ("Poll", "Poll2"):
                        matched = True

                if not matched and "contact" in filter_types:
                    if msg_type == "ContactMessage":
                        matched = True

                if not matched and "event" in filter_types:
                    if msg_type == "Event":
                        matched = True

                if not matched and "edited" in filter_types:
                    if is_edited:
                        matched = True

                if not matched and "forwarded" in filter_types:
                    if has_forwarded:
                        matched = True

                if not matched and "me" in filter_types:
                    if author_guid == my_guid:
                        matched = True

                if not matched and "bots" in filter_types:
                    if author_type == "Bot":
                        matched = True

                if not matched and "users" in filter_types:
                    if author_type == "User":
                        matched = True

                if matched:
                    filtered.append(msg)

        result_dict = {
            "messages": filtered,
            "count": len(filtered),
            "chat_guid": chat_guid,
            "total_all": len(all_messages),
            "filter_types": list(filter_types),
            "member_guids": list(member_guids)
        }
        return Data(result_dict)