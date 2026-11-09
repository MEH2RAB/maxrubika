from .edit_can_called_by import EditCanCalledBy
from .edit_can_join_chat_by import EditCanJoinChatBy
from .edit_show_birthday import EditShowBirthday
from .edit_show_last_online import EditShowLastOnline
from .edit_show_phone_number import EditShowPhoneNumber
from .edit_show_profile_photo import EditShowProfilePhoto
from .get_privacy_setting import GetPrivacySetting
from .set_privacy_setting import SetPrivacySetting
from .set_setting import SetSetting

class Privacy(
    EditCanCalledBy,
    EditCanJoinChatBy,
    EditShowBirthday,
    EditShowLastOnline,
    EditShowPhoneNumber,
    EditShowProfilePhoto,
    GetPrivacySetting,
    SetPrivacySetting,
    SetSetting
):
    pass