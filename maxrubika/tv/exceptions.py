"""Rubika TV Exception Classes for handling API errors."""
import json
from typing import Union, Dict

class TVError(Exception):
    custom_msg = None

    def __init__(self, message: Union[str, Dict, None] = None):
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
            except Exception:
                pass

        self.dev_message = self._custom_user_message or self.dev_message or self._get_custom_msg()
        super().__init__(self.dev_message)

    def _get_custom_msg(self):
        custom_msg = getattr(self.__class__, 'custom_msg', None)
        if isinstance(custom_msg, dict):
            return custom_msg.get('dev_message')
        return None

    def _get_custom_status(self):
        return getattr(self.__class__, 'custom_status', None)

    def __str__(self):
        status = self._get_custom_status()
        if not status:
            status = self.status_det or self.status or "UNKNOWN"

        if status == 'INVALID_AUTH':
            status = 'INVALID_ACCESS'

        dev_message = self.dev_message or "An error occurred."
        return json.dumps({"status": status, "dev_message": dev_message}, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

class InvalidAccess(TVError):
    custom_status = "INVALID_ACCESS"
    custom_msg = {"status": "INVALID_ACCESS", "dev_message": "Access denied. You don't have permission to perform this action."}

class InvalidInput(TVError):
    custom_status = "INVALID_INPUT"
    custom_msg = {"status": "INVALID_INPUT", "dev_message": "Invalid input received. Please check and try again."}

class InvalidSession(TVError):
    custom_status = "INVALID_SESSION"
    custom_msg = {"status": "INVALID_SESSION", "dev_message": "Session parameter is invalid."}

class InvalidAuthInput(TVError):
    custom_status = "INVALID_AUTH_INPUT"
    custom_msg = {"status": "INVALID_AUTH_INPUT", "dev_message": "Authentication parameters are invalid."}

class ServerError(TVError):
    custom_status = "SERVER_ERROR"
    custom_msg = {"status": "SERVER_ERROR", "dev_message": "Server returned an error. Please retry later."}

class TooRequests(TVError):
    custom_status = "TOO_REQUESTS"
    custom_msg = {"status": "TOO_REQUESTS", "dev_message": "Too many requests. Please try again later."}

class NetworkError(TVError):
    custom_status = "NETWORK_ERROR"
    custom_msg = {"status": "NETWORK_ERROR", "dev_message": "A network error occurred. Please check your connection."}

class NotRegistered(TVError):
    custom_status = "NOT_REGISTERED"
    custom_msg = {"status": "NOT_REGISTERED", "dev_message": "User is not registered on TV. Please sign up first."}

class InvalidPlatform(TVError):
    custom_status = "INVALID_PLATFORM"
    custom_msg = {"status": "INVALID_PLATFORM", "dev_message": "Invalid platform specified."}

class InvalidTimeout(TVError):
    custom_status = "INVALID_TIMEOUT"
    custom_msg = {"status": "INVALID_TIMEOUT", "dev_message": "Timeout value is invalid."}

class TimeoutError(TVError):
    custom_status = "TIMEOUT"
    custom_msg = {"status": "TIMEOUT", "dev_message": "Request timed out. Please try again later."}

class NoConnection(TVError):
    custom_status = "NO_CONNECTION"
    custom_msg = {"status": "NO_CONNECTION", "dev_message": "Network connection failed. Please check your internet connection."}

EXCEPTION_MAP = {
    'INVALID_AUTH': InvalidAccess,
    'INVALID_INPUT': InvalidInput,
    'NOT_REGISTERED': NotRegistered,
    'SERVER_ERROR': ServerError,
    'TOO_REQUESTS': TooRequests
}

def raise_exception(status_det: str, result=None):
    exc_class = EXCEPTION_MAP.get(status_det, TVError)
    raise exc_class(result)