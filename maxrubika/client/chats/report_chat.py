from typing import Union
import maxrubika

class ReportChat:
    async def report_chat(
        self: "maxrubika.Client",
        chat: str,
        report_type: Union[int, str],
        description: str = None
    ):
        """
        Report a chat (user, channel, group, etc.) for a specific reason.

        Parameters:
            chat (str): The GUID, link, or username of the chat to be reported.
            report_type (str, int): The type of report.
            description (str, optional): Additional description for the report.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        input = {
            'object_guid': chat_guid,
            'report_type': report_type,
            'report_type_object': 'Object',
            'report_description': description
        }
        return await self.request(method = 'reportObject', input = input)