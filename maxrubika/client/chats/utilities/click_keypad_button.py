import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ClickKeypadButton:
    async def click_keypad_button(
        self: "maxrubika.Messenger",
        chat: str,
        button_id: str
    ):
        """
        Click a button in the chat keypad.

        Parameters:
            chat (str): The GUID, link, or username of the chat (must be a bot).
            button_id (str): The button ID to click.

        Returns:
            The result of the button click.
        """
        from ....data import Data
        from ...exceptions import InvalidInput, InvalidAccess

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith("b0"):
            message = f"'{chat}' does not point to a valid bot. Expected a bot GUID or bot username."
            raise InvalidInput(message)

        bot_info = await self.get_bot_info(chat_guid)

        if isinstance(bot_info, dict):
            bot_info = Data(bot_info)

        chat_keypad = bot_info.find_keys('chat_keypad')

        if not chat_keypad:
            message = f"Bot '{chat}' does not have any keypad buttons."
            raise InvalidAccess(message)

        if isinstance(chat_keypad, dict):
            chat_keypad = Data(chat_keypad)

        rows = chat_keypad.find_keys('rows') or []

        if not rows:
            message = f"Bot '{chat}' does not have any keypad buttons."
            raise InvalidAccess(message)

        button_text = None
        found = False
        available_ids = []

        for row in rows:
            if isinstance(row, dict):
                row = Data(row)

            buttons = row.find_keys('buttons') or []

            for button in buttons:
                if isinstance(button, dict):
                    button = Data(button)

                btn_id = button.find_keys('id')
                btn_text = button.find_keys('button_text')

                if btn_id:
                    available_ids.append(f"{btn_id} ({btn_text})")
                    if btn_id == button_id:
                        button_text = btn_text
                        found = True
                        break

            if found:
                break

        if not found:
            message = f"Button ID '{button_id}' not found in chat keypad. Available buttons: {', '.join(available_ids)}"
            raise InvalidInput(message)

        input_data = {
            'object_guid': chat_guid,
            'rnd': random.randint(100000, 999999),
            'text': button_text,
            'aux_data': {'button_id': button_id}
        }

        return await self.request(
            method='sendMessage',
            input=input_data
        )