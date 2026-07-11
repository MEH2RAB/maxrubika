from typing import Union
import maxrubika

class ReportMessage:
    async def report_message(
        self: "maxrubika.Client",
        chat: str,
        message_id: Union[str, int],
        report_type: Union[int, str],
        description: str = None
    ):
        """
        Report a message for a specific reason.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int]): The ID of the message to be reported.
            report_type (Union[str, int]): The type of report.
            description (str, optional): Additional description for the report.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        input = {
            'object_guid': chat_guid,
            'report_type': report_type,
            'report_type_object': 'Message',
            'report_description': description,
            'message_id': message_id
        }
        return await self.request(method = 'reportObject', input = input)