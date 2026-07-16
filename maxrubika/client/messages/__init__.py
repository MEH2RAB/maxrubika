from .add_reaction import AddReaction
from .auto_delete_message import AutoDeleteMessage
from .click_inline_button import ClickInlineButton
from .click_message_url import ClickMessageUrl
from .delete_all_messages import DeleteAllMessages
from .delete_messages import DeleteMessages
from .delete_my_messages import DeleteMyMessages
from .edit_message import EditMessage
from .forward_messages import ForwardMessages
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
from .get_poll_option_voters import GetPollOptionVoters
from .get_poll_status import GetPollStatus
from .get_scheduled_messages import GetScheduledMessages
from .mark_as_read import MarkAsRead
from .mark_as_seen import MarkAsSeen
from .pin_message import PinMessage
from .remove_reaction import RemoveReaction
from .report_message import ReportMessage
from .request_send_file import RequestSendFile
from .retract_poll import RetractPoll
from .search_chat_messages import SearchChatMessages
from .search_messages import SearchMessages
from .send_contact import SendContact
from .send_file import SendFile
from .send_gif import SendGif
from .send_image import SendImage
from .send_live import SendLive
from .send_location import SendLocation
from .send_message import SendMessage
from .send_message_api_call import SendMessageAPICall
from .send_music import SendMusic
from .send_now_scheduled_message import SendNowScheduledMessage
from .send_poll import SendPoll
from .send_quiz import SendQuiz
from .send_rubino_post import SendRubinoPost
from .send_rubino_story import SendRubinoStory
from .send_sticker import SendSticker
from .send_video import SendVideo
from .send_video_message import SendVideoMessage
from .send_voice import SendVoice
from .stop_poll import StopPoll
from .transcribe_voice import TranscribeVoice
from .unpin_all_messages import UnpinAllMessages
from .unpin_message import UnpinMessage
from .vote_poll import VotePoll

class Messages(
    AddReaction,
    AutoDeleteMessage,
    ClickInlineButton,
    ClickMessageUrl,
    DeleteAllMessages,
    DeleteMessages,
    DeleteMyMessages,
    EditMessage,
    ForwardMessages,
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
    GetPollOptionVoters,
    GetPollStatus,
    GetScheduledMessages,
    MarkAsRead,
    MarkAsSeen,
    PinMessage,
    RemoveReaction,
    ReportMessage,
    RequestSendFile,
    RetractPoll,
    SearchChatMessages,
    SearchMessages,
    SendContact,
    SendFile,
    SendGif,
    SendImage,
    SendLive,
    SendLocation,
    SendMessage,
    SendMessageAPICall,
    SendMusic,
    SendNowScheduledMessage,
    SendPoll,
    SendQuiz,
    SendRubinoPost,
    SendRubinoStory,
    SendSticker,
    SendVideo,
    SendVideoMessage,
    SendVoice,
    StopPoll,
    TranscribeVoice,
    UnpinAllMessages,
    UnpinMessage,
    VotePoll
):
    pass