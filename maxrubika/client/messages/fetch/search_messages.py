from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SearchMessages:
    async def search_messages(
        self: "maxrubika.Messenger",
        chat: str,
        text: str
    ):
        """
        Search for messages containing specific text in a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            text (str): The text to search for.

        Returns:
            The search results.
        """
        from ....data import Data

        chat_guid = await self.get_guid(chat)

        all_data = await self.get_all_messages(chat_guid)

        if isinstance(all_data, dict):
            all_data = Data(all_data)

        all_messages = all_data.find_keys('messages') or []

        matched = []
        text_lower = text.lower()

        for msg in all_messages:
            if isinstance(msg, Data):
                msg = msg.to_dict()

            msg_type = msg.get("type", "")

            if msg_type in ("Text", "FileInlineCaption"):
                msg_text = msg.get("text", "")
                if msg_text and text_lower in msg_text.lower():
                    matched.append(msg)

        result_dict = {
            "messages": matched,
            "count": len(matched),
            "chat_guid": chat_guid,
            "text": text
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)