from .get_poll_option_voters import GetPollOptionVoters
from .get_poll_status import GetPollStatus
from .request_send_file import RequestSendFile
from .retract_poll import RetractPoll
from .stop_poll import StopPoll
from .transcribe_voice import TranscribeVoice
from .vote_poll import VotePoll

class Utilities(
    GetPollOptionVoters,
    GetPollStatus,
    RequestSendFile,
    RetractPoll,
    StopPoll,
    TranscribeVoice,
    VotePoll
):
    pass