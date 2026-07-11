from .get_bot_info import GetBotInfo
from .get_service_info import GetServiceInfo
from .start_bot import StartBot
from .stop_bot import StopBot

class Bots(
    GetBotInfo,
    GetServiceInfo,
    StartBot,
    StopBot
):
    pass