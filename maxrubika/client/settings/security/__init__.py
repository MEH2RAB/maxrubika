from .abort_set_recovery_email import AbortSetRecoveryEmail
from .abort_two_step_setup import AbortTwoStepSetup
from .change_password import ChangePassword
from .check_two_step_passcode import CheckTwoStepPasscode
from .confirm_unconfirmed_session import ConfirmUnconfirmedSession
from .deny_unconfirmed_session import DenyUnconfirmedSession
from .disable_two_step_by_forget_password import DisableTwoStepByForgetPassword
from .get_my_sessions import GetMySessions
from .get_two_passcode_status import GetTwoPasscodeStatus
from .get_unconfirmed_sessions import GetUnconfirmedSessions
from .login_disable_two_step import LoginDisableTwoStep
from .login_two_step_forget_password import LoginTwoStepForgetPassword
from .register_device import RegisterDevice
from .request_forget_password import RequestForgetPassword
from .request_recovery_email import RequestRecoveryEmail
from .resend_code_recovery_email import ResendCodeRecoveryEmail
from .set_two_step_verification import SetTwoStepVerification
from .terminate_other_sessions import TerminateOtherSessions
from .terminate_session import TerminateSession
from .turn_off_two_step import TurnOffTwoStep
from .upgrade_to_api6 import UpgradeToApi6
from .verify_recovery_email import VerifyRecoveryEmail

class Security(
    AbortSetRecoveryEmail,
    AbortTwoStepSetup,
    ChangePassword,
    CheckTwoStepPasscode,
    ConfirmUnconfirmedSession,
    DenyUnconfirmedSession,
    DisableTwoStepByForgetPassword,
    GetMySessions,
    GetTwoPasscodeStatus,
    GetUnconfirmedSessions,
    LoginDisableTwoStep,
    LoginTwoStepForgetPassword,
    RegisterDevice,
    RequestForgetPassword,
    RequestRecoveryEmail,
    ResendCodeRecoveryEmail,
    SetTwoStepVerification,
    TerminateOtherSessions,
    TerminateSession,
    TurnOffTwoStep,
    UpgradeToApi6,
    VerifyRecoveryEmail
):
    pass