import copy
from typing import Optional, Union, Dict, Any, List

class KeypadMixin:
    """Mixin for normalizing keyboard layouts across all send methods."""
    def _normalize_keypad(
        self, 
        keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]], 
        is_inline: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Normalize keyboard data structure for Rubika API."""
        if not keypad:
            return None

        auto_id_counter = 100

        def process_button(btn):
            nonlocal auto_id_counter
            if isinstance(btn, dict):
                btn_copy = btn.copy()
                if "id" not in btn_copy and "button_id" not in btn_copy:
                    btn_copy["id"] = str(auto_id_counter)
                    auto_id_counter += 1

                if "text" in btn_copy and "button_text" not in btn_copy:
                    btn_copy["button_text"] = btn_copy.pop("text")

                if "type" not in btn_copy:
                    btn_copy["type"] = "Simple"
                return btn_copy
            elif isinstance(btn, str):
                new_btn = {
                    "button_text": btn,
                    "type": "Simple",
                    "id": str(auto_id_counter)
                }
                auto_id_counter += 1
                return new_btn
            return btn

        if isinstance(keypad, list):
            rows = []
            for row in keypad:
                if isinstance(row, dict) and "buttons" in row:
                    buttons = [process_button(btn) for btn in row["buttons"]]
                    rows.append({"buttons": buttons})
                else:
                    btn_list = row if isinstance(row, list) else [row]
                    buttons = [process_button(btn) for btn in btn_list]
                    rows.append({"buttons": buttons})
            normalized = {"rows": rows}

        elif isinstance(keypad, dict):
            if "rows" in keypad:
                normalized = copy.deepcopy(keypad)
                for row in normalized.get("rows", []):
                    if "buttons" in row:
                        row["buttons"] = [process_button(btn) for btn in row["buttons"]]
            elif "buttons" in keypad:
                buttons = [process_button(btn) for btn in keypad["buttons"]]
                normalized = {
                    "rows": [{"buttons": buttons}],
                    **{k: v for k, v in keypad.items() if k not in ["buttons"]}
                }
            else:
                return None
        else:
            return None

        if is_inline:
            normalized.pop("resize_keyboard", None)
            normalized.pop("one_time_keyboard", None)

        return normalized