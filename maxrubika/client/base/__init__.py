from .connect import Connect
from .disconnect import Disconnect
from .download_file import DownloadFile
from .get_updates import GetUpdates
from .request import Request
from .run import Run
from .send_code import SendCode
from .sign_in import SignIn
from .start import Start
from .upload_file import UploadFile

class Base(
    Connect,
    Disconnect,
    DownloadFile,
    GetUpdates,
    Request,
    Run,
    SendCode,
    SignIn,
    Start,
    UploadFile
):
    pass