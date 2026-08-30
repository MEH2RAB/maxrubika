from ...data import Data

class MessageResult(Data):
    """Wrapper for message results with action methods."""
    def __init__(self, client, chat_guid, message_id, result_data=None):
        super().__init__(result_data or {})
        self.client = client
        self.chat_guid = chat_guid
        self.message_id = message_id

    def edit(self, text: str, **extras):
        return self.client.edit_message(self.chat_guid, self.message_id, text=text, **extras)

    def delete(self):
        return self.client.delete_messages(self.chat_guid, [self.message_id])

    def reply(self, text: str, **extras):
        return self.client.send_message(self.chat_guid, text=text, reply_to_message_id=self.message_id, **extras)

    def forward(self, to_chat: str = None, **extras):
        return self.client.forward_messages(self.chat_guid, [self.message_id], to_chat or self.chat_guid, **extras)

    def pin(self):
        return self.client.pin_message(self.chat_guid, self.message_id)

    def unpin(self):
        return self.client.unpin_message(self.chat_guid, self.message_id)

    def __repr__(self):
        return f"<MessageResult message_id={self.message_id!r}>"