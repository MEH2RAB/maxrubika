from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetContacts:
    async def get_contacts(
        self: "maxrubika.Messenger",
        show_user_guids: bool = False,
        show_phone_numbers: bool = False,
        all_pages: bool = True,
        start_id: Optional[str] = None
    ):
        """
        Get a list of all contacts.

        Parameters:
            show_user_guids (bool, optional): Show user GUIDs in output. Default is False.
            show_phone_numbers (bool, optional): Show phone numbers in output. Default is False.
            all_pages (bool, optional): If True, automatically fetch all pages of contacts. If False, only fetch one page using start_id. Default is True.
            start_id (str, optional): Starting user ID for pagination. Only used when all_pages is False or as the initial point.

        Returns:
            The result containing all contacts with total count.
        """
        from ...data import Data

        if not all_pages:
            return await self.request(
                method='getContacts',
                input={'start_id': start_id}
            )

        total = 0
        all_users = []
        user_guids = set()
        phone_numbers = set()

        while True:
            result = await self.request(
                method='getContacts',
                input={'start_id': start_id}
            )

            if isinstance(result, dict):
                result = Data(result)

            users = result.find_keys('users') or []

            if not users:
                break

            for user in users:
                user_data = Data(user) if isinstance(user, dict) else user

                user_guid = user_data.find_keys('user_guid')
                phone = user_data.find_keys('phone')

                if user_guid and user_guid not in user_guids:
                    user_guids.add(user_guid)
                    all_users.append(user_data.to_dict())
                    total += 1

                    if phone:
                        formatted_phone = phone if phone.startswith('+') else f"+{phone}"
                        phone_numbers.add(formatted_phone)

            has_continue = result.find_keys('has_continue')
            if not has_continue:
                break

            next_start_id = result.find_keys('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {
            "users": all_users,
            "total": total
        }

        if show_user_guids:
            result_dict["user_guids"] = list(user_guids)

        if show_phone_numbers:
            result_dict["phone_numbers"] = list(phone_numbers)

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)