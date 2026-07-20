import maxrubika

class RequestChangePhoneNumber:
    async def request_change_phone_number(
        self: "maxrubika.Client",
        new_phone_number: str
    ):
        """
        Request to change the account phone number.

        Parameters:
            new_phone_number (str): The new phone number (e.g., 09123456789, +989123456789, +1234567890).

        Returns:
            The result of the API call containing phone_code_hash for verification.
        """
        phone = new_phone_number.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

        if phone.startswith("+"):
            phone = phone[1:]
        elif phone.startswith("00"):
            phone = phone[2:]

        if phone.startswith("09") and len(phone) == 11:
            phone = "98" + phone[1:]

        return await self.request(
            method = 'requestChangePhoneNumber',
            input = {'new_phone_number': phone}
        )