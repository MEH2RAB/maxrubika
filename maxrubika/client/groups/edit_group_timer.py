from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class EditGroupTimer:
    async def edit_group_timer(
        self: "maxrubika.Messenger",
        group: str,
        timer: Union[str, int]
    ):
        """
        Edit the slow mode timer for a group.

        Parameters:
            group (str): The GUID or link of the group.
            timer (Union[str, int]): The new slow mode setting for the group.

        Returns:
            The result of the API call.
        """
        return await self.edit_group_info(group=group, slow_mode=timer)