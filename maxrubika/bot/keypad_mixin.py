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

        used_ids = set()

        def collect_ids(source):
            if isinstance(source, dict):
                if "rows" in source:
                    for row in source.get("rows", []):
                        collect_ids(row)
                elif "buttons" in source:
                    for btn in source["buttons"]:
                        collect_ids(btn)
                else:
                    bid = source.get("id", source.get("button_id"))
                    if bid is not None:
                        used_ids.add(str(bid))
            elif isinstance(source, list):
                for item in source:
                    collect_ids(item)
            elif isinstance(source, (tuple,)):

                if len(source) > 1 and source[1] is not None:
                    used_ids.add(str(source[1]))

        collect_ids(keypad)

        numeric_ids = [int(i) for i in used_ids if i.isdigit()]
        auto_id_counter = max(numeric_ids, default=99) + 1

        def next_id():
            nonlocal auto_id_counter
            while str(auto_id_counter) in used_ids:
                auto_id_counter += 1
            new_id = str(auto_id_counter)
            used_ids.add(new_id)
            auto_id_counter += 1
            return new_id

        def process_button(btn):
            if isinstance(btn, dict):
                btn_copy = btn.copy()

                if "button_id" in btn_copy and "id" not in btn_copy:
                    btn_copy["id"] = btn_copy.pop("button_id")
                elif "button_id" in btn_copy:
                    btn_copy.pop("button_id")

                if "id" not in btn_copy:
                    btn_copy["id"] = next_id()
                else:
                    btn_copy["id"] = str(btn_copy["id"])

                if "text" in btn_copy and "button_text" not in btn_copy:
                    btn_copy["button_text"] = btn_copy.pop("text")

                if "type" not in btn_copy:
                    btn_copy["type"] = "Simple"
                return btn_copy

            elif isinstance(btn, str):
                return {
                    "button_text": btn,
                    "type": "Simple",
                    "id": next_id()
                }

            elif isinstance(btn, (tuple, list)):
                text  = btn[0] if len(btn) > 0 else ""
                bid   = btn[1] if len(btn) > 1 else None
                btype = btn[2] if len(btn) > 2 else None

                result = {
                    "button_text": text,
                    "type": btype if btype is not None else "Simple",
                }

                if bid is None:
                    result["id"] = next_id()
                else:
                    result["id"] = str(bid)

                return result

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