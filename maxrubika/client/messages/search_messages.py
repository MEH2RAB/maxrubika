import maxrubika
from ...data import Data

class SearchMessages:
    async def search_messages(
        self: "maxrubika.Client",
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
        chat_guid = await self.get_guid(chat)

        all_data = await self.get_all_messages(chat_guid)
        all_messages = all_data["messages"]

        matched = []
        text_lower = text.lower()

        for msg in all_messages:
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
        return Data(result_dict)