import maxrubika

class MemberIsAdmin:
    async def member_is_admin(
        self: "maxrubika.Bot",
        chat_id: str,
        user_id: str
    ) -> bool:
        """
        Check whether a member is an admin or owner of the given chat.

        Parameters:
            chat_id (str): chat_id of group (g0...) or channel (c0...).
            user_id (str): user_id of the member (u0...).

        Returns:
            bool: True if status is 'Admin' or 'Creator', else False.
        """
        result = await self.get_chat_member(chat_id, user_id)

        data = result.to_dict() if hasattr(result, "to_dict") else result
        status = data.get("data", {}).get("chat_member", {}).get("status")

        return status in ("Admin", "Creator")