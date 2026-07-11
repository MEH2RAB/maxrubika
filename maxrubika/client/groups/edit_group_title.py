import maxrubika

class EditGroupTitle:
    async def edit_group_title(
        self: "maxrubika.Client",
        group: str,
        title: str
    ):
        """
        Edit title of a group.

        Parameters:
            group (str): The GUID or link of the group.
            title (str): The new title of the group.

        Returns:
            The result of the API call.
        """
        return await self.edit_group_info(group = group, title = title)