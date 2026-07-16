from .on_add_reaction import OnAddReaction
from .on_call_signal import OnCallSignal
from .on_call_update import OnCallUpdate
from .on_chat_updates import OnChatUpdates
from .on_delete_message import OnDeleteMessage
from .on_draft_message import OnDraftMessage
from .on_edit_message import OnEditMessage
from .on_message import OnMessage
from .on_new_message import OnNewMessage
from .on_remove_notifications import OnRemoveNotifications
from .on_remove_reaction import OnRemoveReaction
from .on_scheduled_message import OnScheduledMessage
from .on_show_activities import OnShowActivities
from .on_show_notifications import OnShowNotifications
from .on_unconfirmed_session import OnUnconfirmedSession
from .on_voice_chat_participant import OnVoiceChatParticipant
from .on_voice_chat_update import OnVoiceChatUpdate

class Decorators(
    OnAddReaction,
    OnCallSignal,
    OnCallUpdate,
    OnChatUpdates,
    OnDeleteMessage,
    OnDraftMessage,
    OnEditMessage,
    OnMessage,
    OnNewMessage,
    OnRemoveNotifications,
    OnRemoveReaction,
    OnScheduledMessage,
    OnShowActivities,
    OnShowNotifications,
    OnUnconfirmedSession,
    OnVoiceChatParticipant,
    OnVoiceChatUpdate
):
    pass