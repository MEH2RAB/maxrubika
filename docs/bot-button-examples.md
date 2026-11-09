# نمونه‌های عملی

---

## ساخت دکمهٔ ساده

```python
simple_button = {
    "id": "1",
    "type": "Simple",
    "button_text": "کلیک کنید"
}
```

---

## ساخت دکمهٔ انتخاب از لیست

```python
selection_button = {
    "id": "2",
    "type": "Selection",
    "button_text": "انتخاب رنگ",
    "button_selection": {
        "selection_id": "color_picker",
        "search_type": "Local",
        "get_type": "Local",
        "is_multi_selection": False,
        "columns_count": "2",
        "title": "رنگ مورد نظر را انتخاب کنید",
        "items": [
            {"text": "قرمز", "type": "TextOnly"},
            {"text": "آبی", "type": "TextOnly"},
            {"text": "سبز", "type": "TextOnly"}
        ]
    }
}
```

---

## ساخت دکمهٔ تقویم

```python
calendar_button = {
    "id": "3",
    "type": "Calendar",
    "button_text": "انتخاب تاریخ",
    "button_calendar": {
        "type": "DatePersian",
        "min_year": "1400",
        "max_year": "1410",
        "title": "تاریخ تولد خود را انتخاب کنید"
    }
}
```

---

## ساخت دکمهٔ ورودی متن

```python
textbox_button = {
    "id": "4",
    "type": "Textbox",
    "button_text": "نظر خود را بنویسید",
    "button_textbox": {
        "type_line": "MultiLine",
        "type_keypad": "String",
        "place_holder": "نظر خود را اینجا وارد کنید...",
        "title": "فرم نظرسنجی"
    }
}
```

---

<div style="display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap;">

<a href="../bot-more/" class="md-button" style="background: #ffffff; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 140px; display: flex; align-items: center; justify-content: center; text-align: center; padding: 10px 20px; font-weight: bold; color: #333;">بازگشت به توضیحات بیشتر</a>

</div>