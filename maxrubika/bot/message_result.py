from ..data import Data

class MessageResult(Data):
    """Wrapper for bot message results with action methods."""
    def __new__(cls, bot, chat_id, message_id, result_data=None):
        if getattr(bot, 'as_dict', False):
            data = result_data.to_dict() if isinstance(result_data, Data) else (result_data or {})
            return Data.clean(dict(data))
        return super().__new__(cls)

    def __init__(self, bot, chat_id, message_id, result_data=None):
        if isinstance(result_data, Data):
            result_data = result_data.to_dict()

        super().__init__(result_data or {})
        self.bot = bot
        self.chat_id = chat_id
        self.message_id = message_id

    async def edit(self, text: str, **extras):
        return await self.bot.edit_message(
            self.chat_id,
            self.message_id,
            text=text,
            **extras
        )

    async def delete(self):
        return await self.bot.delete_message(
            self.chat_id,
            self.message_id
        )

    async def reply(self, text: str, **extras):
        return await self.bot.send_message(
            self.chat_id,
            text=text,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def forward(self, to_chat_id: str = None):
        return await self.bot.forward_message(
            self.chat_id,
            self.message_id,
            to_chat_id or self.chat_id
        )

    def __repr__(self):
        return f"<MessageResult chat_id={self.chat_id!r} message_id={self.message_id!r}>"