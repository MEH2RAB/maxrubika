from .get_all_messages import GetAllMessages
from .get_chat_messages import GetChatMessages
from .get_first_message import GetFirstMessage
from .get_first_messages import GetFirstMessages
from .get_last_message import GetLastMessage
from .get_last_messages import GetLastMessages
from .get_message_info import GetMessageInfo
from .get_message_url import GetMessageUrl
from .get_messages import GetMessages
from .get_messages_by_id import GetMessagesByID
from .get_messages_interval import GetMessagesInterval
from .get_messages_reactions import GetMessagesReactions
from .get_messages_updates import GetMessagesUpdates
from .get_pinned_messages import GetPinnedMessages
from .get_scheduled_messages import GetScheduledMessages
from .get_wallet_transfer_message import GetWalletTransferMessage
from .search_chat_messages import SearchChatMessages
from .search_global_messages import SearchGlobalMessages
from .search_messages import SearchMessages

class Fetch(
    GetAllMessages,
    GetChatMessages,
    GetFirstMessage,
    GetFirstMessages,
    GetLastMessage,
    GetLastMessages,
    GetMessageInfo,
    GetMessageUrl,
    GetMessages,
    GetMessagesByID,
    GetMessagesInterval,
    GetMessagesReactions,
    GetMessagesUpdates,
    GetPinnedMessages,
    GetScheduledMessages,
    GetWalletTransferMessage,
    SearchChatMessages,
    SearchGlobalMessages,
    SearchMessages
):
    pass