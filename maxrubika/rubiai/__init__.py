from ..hybrid import wrap_methods

from .delete_session import DeleteSession
from .download_image import DownloadImage
from .edit_session import EditSession
from .get_chat_history import GetChatHistory
from .get_feedback_issues import GetFeedbackIssues
from .get_service_access import GetServiceAccess
from .get_sessions import GetSessions
from .get_welcome import GetWelcome
from .request import Request
from .send_feedback import SendFeedback
from .send_message import SendMessage
from .send_message_stream import SendMessageStream
from .set_feedback_detail import SetFeedbackDetail
from .speech_to_text import SpeechToText
from .stop_session_stream import StopSessionStream

class Methods(
    DeleteSession,
    DownloadImage,
    EditSession,
    GetChatHistory,
    GetFeedbackIssues,
    GetServiceAccess,
    GetSessions,
    GetWelcome,
    Request,
    SendFeedback,
    SendMessage,
    SendMessageStream,
    SetFeedbackDetail,
    SpeechToText,
    StopSessionStream
):
    pass

wrap_methods(Methods)