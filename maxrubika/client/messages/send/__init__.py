from .save_message_draft import SaveMessageDraft
from .send_contact import SendContact
from .send_file import SendFile
from .send_gif import SendGif
from .send_image import SendImage
from .send_live import SendLive
from .send_live_location import SendLiveLocation
from .send_location import SendLocation
from .send_message import SendMessage
from .send_message_api_call import SendMessageAPICall
from .send_music import SendMusic
from .send_now_scheduled_message import SendNowScheduledMessage
from .send_poll import SendPoll
from .send_quiz import SendQuiz
from .send_rubino_post import SendRubinoPost
from .send_rubino_product import SendRubinoProduct
from .send_rubino_story import SendRubinoStory
from .send_sticker import SendSticker
from .send_video import SendVideo
from .send_video_message import SendVideoMessage
from .send_voice import SendVoice
from .send_wallet_transfer_message import SendWalletTransferMessage

class Send(
    SaveMessageDraft,
    SendContact,
    SendFile,
    SendGif,
    SendImage,
    SendLive,
    SendLiveLocation,
    SendLocation,
    SendMessage,
    SendMessageAPICall,
    SendMusic,
    SendNowScheduledMessage,
    SendPoll,
    SendQuiz,
    SendRubinoPost,
    SendRubinoProduct,
    SendRubinoStory,
    SendSticker,
    SendVideo,
    SendVideoMessage,
    SendVoice,
    SendWalletTransferMessage
):
    pass