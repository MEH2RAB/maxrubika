from typing import Union, List, Optional
import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class UnbanAllMembers:
    async def unban_all_members(
        self: "maxrubika.Client",
        chat: str,
        exclude: Optional[Union[str, List[str]]] = None
    ):
        """
        Unban all banned members in a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the group or channel.
            exclude (Optional[Union[str, List[str]]]): Member GUID(s) or username(s) to exclude from unban. Default is None.

        Returns:
            Result of unban operation.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        banned_result = await self.get_banned_members(chat_guid, show_member_guids=True)

        if not banned_result.member_guids:
            return Data({"status": "OK", "message": "No banned members found."})

        exclude_list = []
        if exclude is not None:
            if isinstance(exclude, str):
                exclude_list.append(exclude)
            elif isinstance(exclude, list):
                exclude_list.extend(exclude)

        exception_guids = []

        if exclude_list:
            for member in exclude_list:
                member_guid = await self.get_guid(member)

                if not member_guid.startswith(("u0", "b0")):
                    message = f"'{member}' does not point to a valid user or bot. Expected a user GUID, bot GUID, or username."
                    raise InvalidInput(message)

                exception_guids.append(member_guid)

        final_guids = [guid for guid in banned_result.member_guids if guid not in exception_guids]

        if not final_guids:
            return Data({"status": "OK", "message": "All banned members are in exceptions list. No one to unban."})

        total = len(banned_result.member_guids)
        excluded = len(exception_guids)
        to_unban = len(final_guids)

        await self.unban_members(chat_guid, final_guids)

        return Data({
            "status": "OK",
            "total_banned": total,
            "excluded": excluded,
            "unbanned": to_unban
        })