import typing
import maxrubika

class EditGroupTimer:
    async def edit_group_timer(
        self: "maxrubika.Client",
        group: str,
        timer: typing.Union[str, int]
    ):
        """
        Parameters:
            group (str): The GUID or link of the group.
            timer (Union[str, int]): The new slow mode setting for the group.

        Returns:
            The result of the API call.
        """
        return await self.edit_group_info(group = group, slow_mode = timer)