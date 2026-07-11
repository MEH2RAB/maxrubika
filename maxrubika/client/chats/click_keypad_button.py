import random
import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class ClickKeypadButton:
    async def click_keypad_button(
        self: "maxrubika.Client",
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
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith("b0"):
            message = f"'{chat}' does not point to a valid bot. Expected a bot GUID or bot username."
            raise InvalidInput(message)

        bot_info = await self.get_bot_info(chat_guid)
        bot_data = bot_info.to_dict() if hasattr(bot_info, 'to_dict') else bot_info

        chat_obj = bot_data.get('chat', {})
        chat_keypad = chat_obj.get('chat_keypad')

        if not chat_keypad:
            return Data({"status": "ERROR", "message": f"Bot '{chat}' does not have any keypad buttons."})

        rows = chat_keypad.get('rows', [])
        if not rows:
            return Data({"status": "ERROR", "message": f"Bot '{chat}' does not have any keypad buttons."})

        button_text = None
        found = False
        available_ids = []

        for row in rows:
            for button in row.get('buttons', []):
                btn_id = button.get('id')
                btn_text = button.get('button_text')
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

        return await self.request(
            method = 'sendMessage',
            input = {
                'object_guid': chat_guid,
                'rnd': random.randint(100000, 999999),
                'text': button_text,
                'aux_data': {'button_id': button_id}
            }
        )