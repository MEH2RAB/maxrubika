from .add_folder import AddFolder
from .auto_delete_account import AutoDeleteAccount
from .change_password import ChangePassword
from .check_two_step_passcode import CheckTwoStepPasscode
from .delete_account import DeleteAccount
from .delete_folder import DeleteFolder
from .edit_can_called_by import EditCanCalledBy
from .edit_can_join_chat_by import EditCanJoinChatBy
from .edit_show_birthday import EditShowBirthday
from .edit_show_last_online import EditShowLastOnline
from .edit_show_phone_number import EditShowPhoneNumber
from .edit_show_profile_photo import EditShowProfilePhoto
from .get_folders import GetFolders
from .get_my_sessions import GetMySessions
from .get_notification_setting import GetNotificationSetting
from .get_privacy_setting import GetPrivacySetting
from .get_suggested_folders import GetSuggestedFolders
from .get_two_passcode_status import GetTwoPasscodeStatus
from .logout import Logout
from .recovery_email import RecoveryEmail
from .register_device import RegisterDevice
from .set_notification import SetNotification
from .set_setting import SetSetting
from .set_two_step_verification import SetTwoStepVerification
from .terminate_other_sessions import TerminateOtherSessions
from .terminate_session import TerminateSession
from .turn_off_two_step import TurnOffTwoStep
from .update_my_bio import UpdateMyBio
from .update_my_birthday import UpdateMyBirthday
from .update_my_name import UpdateMyName
from .update_my_profile import UpdateMyProfile
from .update_my_username import UpdateMyUsername

class Settings(
    AddFolder,
    AutoDeleteAccount,
    ChangePassword,
    CheckTwoStepPasscode,
    DeleteAccount,
    DeleteFolder,
    EditCanCalledBy,
    EditCanJoinChatBy,
    EditShowBirthday,
    EditShowLastOnline,
    EditShowPhoneNumber,
    EditShowProfilePhoto,
    GetFolders,
    GetMySessions,
    GetNotificationSetting,
    GetPrivacySetting,
    GetSuggestedFolders,
    GetTwoPasscodeStatus,
    Logout,
    RecoveryEmail,
    RegisterDevice,
    SetNotification,
    SetSetting,
    SetTwoStepVerification,
    TerminateOtherSessions,
    TerminateSession,
    TurnOffTwoStep,
    UpdateMyBio,
    UpdateMyBirthday,
    UpdateMyName,
    UpdateMyProfile,
    UpdateMyUsername
):
    pass