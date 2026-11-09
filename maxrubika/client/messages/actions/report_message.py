from typing import Union, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

REPORT_TYPE_MAP = {
    "other": 100,
    "violence": 101,
    "spam": 102,
    "porn": 103,
    "childabuse": 104,
    "child_abuse": 104,
    "copyright": 105,
    "fraud": 106
}

class ReportMessage:
    async def report_message(
        self: "maxrubika.Messenger",
        chat: str,
        message_id: Union[str, int],
        report_type: Union[int, str],
        description: Optional[str] = None
    ):
        """
        Report a message for a specific reason.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int]): The ID of the message to be reported.
            report_type (Union[int, str]): The report reason. Can be int (100-106) or str name (case-insensitive): 'Other', 'Violence', 'Spam', 'Porn', 'ChildAbuse', 'Copyright', 'Fraud'. If 100 (Other), 'description' is required.
            description (str, optional): Description for the report. Required when report_type is 100 (Other).

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if isinstance(report_type, str):
            key = report_type.strip().lower()
            if key.isdigit():
                report_type = int(key)
            elif key in REPORT_TYPE_MAP:
                report_type = REPORT_TYPE_MAP[key]
            else:
                message = f"Invalid 'report_type': '{report_type}'. Must be an integer between 100 and 106, or one of: Other, Violence, Spam, Porn, ChildAbuse, Copyright, Fraud."
                raise InvalidInput(message)

        if not isinstance(report_type, int) or not (100 <= report_type <= 106):
            raise InvalidInput("'report_type' must be an integer between 100 and 106.")

        if report_type == 100 and not description:
            raise InvalidInput("'description' is required when 'report_type' is 100 (Other).")

        input_data = {
            'object_guid': chat_guid,
            'report_type': report_type,
            'report_type_object': 'Message',
            'message_id': message_id
        }
        if report_type == 100:
            input_data['report_description'] = description

        return await self.request(method='reportObject', input=input_data)