from .add_reaction import AddReaction
from .auto_delete_message import AutoDeleteMessage
from .click_inline_button import ClickInlineButton
from .click_message_url import ClickMessageUrl
from .delete_all_messages import DeleteAllMessages
from .delete_message import DeleteMessage
from .delete_messages import DeleteMessages
from .delete_my_messages import DeleteMyMessages
from .edit_message import EditMessage
from .forward_message import ForwardMessage
from .forward_messages import ForwardMessages
from .mark_as_read import MarkAsRead
from .mark_as_seen import MarkAsSeen
from .pin_message import PinMessage
from .remove_reaction import RemoveReaction
from .report_message import ReportMessage
from .unpin_all_messages import UnpinAllMessages
from .unpin_message import UnpinMessage

class Actions(
    AddReaction,
    AutoDeleteMessage,
    ClickInlineButton,
    ClickMessageUrl,
    DeleteAllMessages,
    DeleteMessage,
    DeleteMessages,
    DeleteMyMessages,
    EditMessage,
    ForwardMessage,
    ForwardMessages,
    MarkAsRead,
    MarkAsSeen,
    PinMessage,
    RemoveReaction,
    ReportMessage,
    UnpinAllMessages,
    UnpinMessage
):
    pass