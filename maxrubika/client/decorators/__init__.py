from .on_add_reaction import OnAddReaction
from .on_chat_updates import OnChatUpdates
from .on_delete_message import OnDeleteMessage
from .on_edit_message import OnEditMessage
from .on_message import OnMessage
from .on_new_message import OnNewMessage
from .on_remove_notifications import OnRemoveNotifications
from .on_remove_reaction import OnRemoveReaction
from .on_show_activities import OnShowActivities
from .on_show_notifications import OnShowNotifications

class Decorators(
    OnAddReaction,
    OnChatUpdates,
    OnDeleteMessage,
    OnEditMessage,
    OnMessage,
    OnNewMessage,
    OnRemoveNotifications,
    OnRemoveReaction,
    OnShowActivities,
    OnShowNotifications
):
    pass