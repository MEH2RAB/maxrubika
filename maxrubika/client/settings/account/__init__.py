from .auto_delete_account import AutoDeleteAccount
from .delete_account import DeleteAccount
from .get_user_setting import GetUserSetting
from .request_change_phone_number import RequestChangePhoneNumber
from .update_my_bio import UpdateMyBio
from .update_my_birthday import UpdateMyBirthday
from .update_my_name import UpdateMyName
from .update_my_profile import UpdateMyProfile
from .update_my_username import UpdateMyUsername
from .verify_change_phone_number import VerifyChangePhoneNumber

class Account(
    AutoDeleteAccount,
    DeleteAccount,
    GetUserSetting,
    RequestChangePhoneNumber,
    UpdateMyBio,
    UpdateMyBirthday,
    UpdateMyName,
    UpdateMyProfile,
    UpdateMyUsername,
    VerifyChangePhoneNumber
):
    pass