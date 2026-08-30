from ..data import Data


class MessageResult(Data):
    """Wrapper for bot message results with action methods."""

    def __init__(self, bot, chat_id, message_id, result_data=None):
        super().__init__(result_data or {})
        self.bot = bot
        self.chat_id = chat_id
        self.message_id = message_id

    def edit(self, text: str, **extras):
        return self.bot.edit_message(
            self.chat_id,
            self.message_id,
            text=text,
            **extras
        )

    def delete(self):
        return self.bot.delete_message(
            self.chat_id,
            self.message_id
        )

    def reply(self, text: str, **extras):
        return self.bot.send_message(
            self.chat_id,
            text=text,
            reply_to_message_id=self.message_id,
            **extras
        )

    def forward(self, to_chat_id: str = None):
        return self.bot.forward_message(self.chat_id, self.message_id, to_chat_id or self.chat_id)

    def __repr__(self):
        return f"<MessageResult message_id={self.message_id!r}>"