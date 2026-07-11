"""
Rubika Client Exception Classes for handling API errors.
"""
import json
from typing import Optional, Union, Dict

class ClientError(Exception):
    def __init__(self, message=None, request=None):
        if message is None:
            message = "An unknown client error occurred."
        self.request = request
        super().__init__(message)

class StopHandler(ClientError): pass
class CancelledError(ClientError): pass

class NetworkError(Exception):
    def __init__(self, message=None, request=None):
        self.dev_message = message or "A network error occurred."
        self.request = request
        super().__init__(self.dev_message)
    
    def __str__(self) -> str:
        return json.dumps({
            "status": "NETWORK_ERROR",
            "dev_message": self.dev_message
        }, ensure_ascii=False)
    
    def __repr__(self) -> str:
        return self.__str__()

class RequestError(ClientError):
    def __init__(self, message: Union[str, Dict, None] = None, request=None):
        self.request = request
        self.status = None
        self.status_det = None
        self.dev_message = None
        self._custom_user_message = None

        if isinstance(message, str):
            self._custom_user_message = message

        if isinstance(message, dict):
            self.status = message.get('status', 'UNKNOWN')
            self.status_det = message.get('status_det', 'UNKNOWN')

            if self.status_det == 'INVALID_AUTH':
                self.status_det = 'INVALID_ACCESS'

            try:
                csm = message.get('client_show_message', {})
                if csm:
                    self.dev_message = csm.get('link', {}).get('alert_data', {}).get('message')
            except:
                pass

            result_message = message
        else:
            result_message = message or self._get_custom_msg()

        super().__init__(result_message, request)

    def _get_custom_msg(self) -> Optional[str]:
        custom_msg = getattr(self.__class__, 'custom_msg', None)
        if custom_msg:
            try:
                custom_json = json.loads(custom_msg)
                return custom_json.get('dev_message')
            except:
                return None
        return None

    def _get_custom_status(self) -> Optional[str]:
        return getattr(self.__class__, 'custom_status', None)

    def __str__(self) -> str:
        status = self._get_custom_status()
        if not status:
            status = self.status_det or self.status or "UNKNOWN"

        if status == 'INVALID_AUTH':
            status = 'INVALID_ACCESS'

        dev_message = None
        if self._custom_user_message:
            dev_message = self._custom_user_message
        elif self.dev_message:
            dev_message = self.dev_message
        else:
            dev_message = self._get_custom_msg()

        if not dev_message:
            dev_message = "An error occurred."

        return json.dumps({
            "status": status,
            "dev_message": dev_message
        }, ensure_ascii=False)

    def __repr__(self) -> str:
        return self.__str__()

class InvalidInput(RequestError):
    custom_status = "INVALID_INPUT"
    custom_msg = '{"status": "INVALID_INPUT", "dev_message": "Invalid input received. Please check and try again."}'

class InvalidAccess(RequestError):
    custom_status = "INVALID_ACCESS"
    custom_msg = '{"status": "INVALID_ACCESS", "dev_message": "Access denied. You don\'t have permission to perform this action."}'

InvalidAuth = InvalidAccess

class TooRequests(RequestError):
    custom_status = "TOO_REQUESTS"
    custom_msg = '{"status": "TOO_REQUESTS", "dev_message": "Too many requests. Please try again later."}'

class ServerError(RequestError):
    custom_status = "SERVER_ERROR"
    custom_msg = '{"status": "SERVER_ERROR", "dev_message": "Server returned an error. Please retry later."}'

class NotRegistered(RequestError):
    custom_status = "NOT_REGISTERED"
    custom_msg = '{"status": "NOT_REGISTERED", "dev_message": "The user is not registered. Please register first."}'

class CodeIsExpired(RequestError):
    custom_status = "CODE_IS_EXPIRED"
    custom_msg = '{"status": "CODE_IS_EXPIRED", "dev_message": "This code has expired."}'

class UsernameExist(RequestError):
    custom_status = "USERNAME_EXIST"
    custom_msg = '{"status": "USERNAME_EXIST", "dev_message": "This username already exists."}'

class InvalidChatInput(RequestError):
    custom_status = "INVALID_CHAT_INPUT"
    custom_msg = '{"status": "INVALID_CHAT_INPUT", "dev_message": "Unable to determine chat type from input. Please provide a valid username, link, or GUID."}'

class InvalidGroupLink(RequestError):
    custom_status = "INVALID_GROUP_LINK"
    custom_msg = '{"status": "INVALID_GROUP_LINK", "dev_message": "The provided link is not a valid group link or the group does not exist."}'

class InvalidChannelLink(RequestError):
    custom_status = "INVALID_CHANNEL_LINK"
    custom_msg = '{"status": "INVALID_CHANNEL_LINK", "dev_message": "The provided link is not a valid channel link or the channel does not exist."}'

class InvalidUsername(RequestError):
    custom_status = "INVALID_USERNAME"
    custom_msg = '{"status": "INVALID_USERNAME", "dev_message": "The username does not exist or is invalid."}'

class CodeIsUsed(RequestError): pass
class ErrorAction(RequestError): pass
class ErrorIgnore(RequestError): pass
class UrlNotFound(RequestError): pass
class NoConnection(RequestError): pass
class Undeliverable(RequestError): pass
class InvalidMethod(RequestError): pass
class ErrorTryAgain(RequestError): pass
class ErrorMessageTry(RequestError): pass
class ErrorMessageIgn(RequestError): pass
class InternalProblem(RequestError): pass
class NotSupportedApiVersion(RequestError): pass

class UploadError(Exception):
    def __init__(self, status, status_det, dev_message: str = None):
        self.status = status
        self.status_det = status_det
        self.dev_message = dev_message

EXCEPTION_MAP = {
    'INVALID_INPUT': InvalidInput, 'INVALID_AUTH': InvalidAccess,
    'TOO_REQUESTS': TooRequests, 'SERVER_ERROR': ServerError,
    'NOT_REGISTERED': NotRegistered, 'URL_NOT_FOUND': UrlNotFound,
    'CODE_IS_USED': CodeIsUsed, 'ERROR_ACTION': ErrorAction,
    'ERROR_IGNORE': ErrorIgnore, 'NO_CONNECTION': NoConnection,
    'UNDELIVERABLE': Undeliverable, 'CODE_IS_EXPIRED': CodeIsExpired,
    'INVALID_METHOD': InvalidMethod, 'USERNAME_EXIST': UsernameExist,
    'ERROR_TRY_AGAIN': ErrorTryAgain, 'ERROR_MESSAGE_TRY': ErrorMessageTry,
    'INTERNAL_PROBLEM': InternalProblem, 'ERROR_MESSAGE_IGN': ErrorMessageIgn,
    'NOT_SUPPORTED_API_VERSION': NotSupportedApiVersion, 'INVALID_CHAT_INPUT': InvalidChatInput,
    'INVALID_GROUP_LINK': InvalidGroupLink, 'INVALID_CHANNEL_LINK': InvalidChannelLink,
    'INVALID_USERNAME': InvalidUsername,
}

def get(status_det: str):
    return EXCEPTION_MAP.get(status_det, ClientError)

def raise_exception(status_det: str, result=None, request=None):
    exc_class = EXCEPTION_MAP.get(status_det, ClientError)
    raise exc_class(result, request=request)