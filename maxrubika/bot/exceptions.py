"""
Rubika Bot Exception classes for handling API errors.
"""
import json

class APIException(Exception):
    def __init__(self, status: str, dev_message: any = None):
        self.status = status

        if dev_message is None:
            dev_message = self._get_default_message(status)
        self.dev_message = dev_message
        super().__init__(self.__str__())

    @classmethod
    def from_response(cls, response_data: dict):
        status = response_data.get("status")
        dev_message = response_data.get("dev_message")

        if not status:
            status = "UNKNOWN_ERROR"

        exception_map = {
            "SERVER_ERROR": ServerError,
            "INVALID_INPUT": InvalidInput,
            "INVALID_ACCESS": InvalidAccess,
            "TOO_REQUESTS": TooRequests,
        }
        exception_class = exception_map.get(status, cls)
        return exception_class(status=status, dev_message=dev_message)

    def _get_default_message(self, status: str) -> str:
        default_messages = {
            "SERVER_ERROR": "Server returned an error. Please retry later.",
            "INVALID_INPUT": "Invalid input received. Please check and try again.",
            "INVALID_ACCESS": "Access denied. You don't have permission to perform this action.",
            "TOO_REQUESTS": "Too many requests. Please slow down and try again later.",
        }

        if status in default_messages:
            return default_messages[status]

        return f"An error occurred: {status}"

    def __str__(self):
        error_data = {"status": self.status}
        if self.dev_message:
            error_data["dev_message"] = self.dev_message
        return json.dumps(error_data, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

class Network(APIException):
    """خطاهای مربوط به شبکه و اتصال"""
    def __init__(self, dev_message: any = None):
        super().__init__(status="NETWORK_ERROR", dev_message=dev_message)

class Timeout(APIException):
    """خطای timeout در درخواست‌ها"""
    def __init__(self, dev_message: any = None):
        super().__init__(status="TIMEOUT_ERROR", dev_message=dev_message)

class BadGateway(APIException):
    """خطای 502 Bad Gateway"""
    def __init__(self, dev_message: any = None):
        super().__init__(status="BAD_GATEWAY", dev_message=dev_message)

class InvalidResponse(APIException):
    """پاسخ نامعتبر یا غیرقابل پردازش از سرور"""
    def __init__(self, dev_message: any = None):
        super().__init__(status="INVALID_RESPONSE", dev_message=dev_message)

class JSONDecode(APIException):
    """خطا در پردازش JSON پاسخ"""
    def __init__(self, dev_message: any = None):
        super().__init__(status="JSON_DECODE_ERROR", dev_message=dev_message)

class ServerError(APIException):
    """خطای سرور (خطاهای داخلی سرور روبیکا)"""
    def __init__(self, dev_message: any = None):
        super().__init__(status="SERVER_ERROR", dev_message=dev_message)

class InvalidInput(APIException):
    """ورودی نامعتبر - پارامترهای ارسالی مشکل دارند"""
    def __init__(self, dev_message: any = None):
        super().__init__(status="INVALID_INPUT", dev_message=dev_message)

class InvalidAccess(APIException):
    """دسترسی نامعتبر - توکن نامعتبر یا دسترسی کافی نیست"""
    def __init__(self, dev_message: any = None):
        super().__init__(status="INVALID_ACCESS", dev_message=dev_message)

class TooRequests(APIException):
    """تعداد درخواست‌ها بیش از حد مجاز - Rate limit"""
    def __init__(self, dev_message: any = None):
        super().__init__(status="TOO_REQUESTS", dev_message=dev_message)