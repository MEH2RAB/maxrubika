from typing import Optional, Union
import maxrubika
from ..exceptions import InvalidInput

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

class ReportLive:
    async def report_live(
        self: "maxrubika.Client",
        live_id: str,
        report_type: Union[int, str],
        description: Optional[str] = None
    ):
        """
        Report a live stream.

        Parameters:
            live_id (str): The ID of the live stream to report.
            report_type (Union[int, str]): The report reason.
                Can be:
                    - Integer code between 100 and 106
                    - String name (case-insensitive): 'Other', 'Violence',
                      'Spam', 'Porn', 'ChildAbuse', 'Copyright', 'Fraud'
                If set to 100 (Other), `description` becomes required.
            description (Optional[str]): Description for the report.
                Required when `report_type` is 100 (Other).

        Returns:
            The result of the API call.
        """
        if isinstance(report_type, str):
            key = report_type.strip().lower()
            if key.isdigit():
                report_type = int(key)
            elif key in REPORT_TYPE_MAP:
                report_type = REPORT_TYPE_MAP[key]
            else:
                raise InvalidInput(
                    f"Invalid 'report_type': '{report_type}'. "
                    f"Must be an integer between 100 and 106, or one of: "
                    f"Other, Violence, Spam, Porn, ChildAbuse, Copyright, Fraud.")

        if not isinstance(report_type, int) or not (100 <= report_type <= 106):
            raise InvalidInput(
                "'report_type' must be an integer between 100 and 106.")

        if report_type == 100 and not description:
            raise InvalidInput(
                "'description' is required when 'report_type' is 100 (Other).")

        input_data = {
            "report_object_type": "Live",
            "report_type": report_type,
            "live_id": live_id
        }
        if report_type == 100:
            input_data["report_description"] = description

        return await self.request(method = 'reportObject', input = input_data)