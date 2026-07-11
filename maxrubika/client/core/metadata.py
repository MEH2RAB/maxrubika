import re
from typing import Dict, List, Any

MARKDOWN_RE = re.compile(
    r"(?:^(?:> ?[^\n]*\n?)+)|```([\s\S]*?)```|\*\*([^\n*]+?)\*\*|`([^\n`]+?)`|__([^\n_]+?)__|--([^\n-]+?)--|~~([^\n~]+?)~~|\|\|([^\n|]+?)\|\||\[([^\]]+?)\]\((\S+)\)",
    flags=re.DOTALL | re.MULTILINE,
)

MARKDOWN_TYPES = {
    ">": ("Quote", None),
    "```": ("Pre", 1),
    "**": ("Bold", 2),
    "`": ("Mono", 3),
    "__": ("Italic", 4),
    "--": ("Underline", 5),
    "~~": ("Strike", 6),
    "||": ("Spoiler", 7),
    "[": ("Link", 8),
}

MARKDOWN_TYPE_SEQUENCE = tuple(MARKDOWN_TYPES.items())

def _utf16_len(text: str) -> List[int]:
    lens = [0]
    total = 0
    for ch in text:
        total += 2 if ord(ch) > 0xFFFF else 1
        lens.append(total)
    return lens

def _is_in_username(text: str, position: int) -> bool:
    i = position - 1
    found_at = False
    
    while i >= 0:
        if text[i] == '@':
            found_at = True
            break
        elif text[i] in ' \n':
            break
        i -= 1
    
    if not found_at:
        return False
    
    j = position
    while j < len(text) and text[j] not in ' \n':
        j += 1
    
    return position < j

def to_metadata(text: str) -> Dict[str, Any]:
    """تبدیل Markdown به metadata برای Rubika API"""
    parts = []
    current = text
    offset = 0
    char_offset = 0
    utf16 = _utf16_len(text)

    for match in MARKDOWN_RE.finditer(text):
        group = match.group()
        start, end = match.span()
        
        if group.startswith('__'):
            if _is_in_username(text, start):
                continue
        
        adj_start = utf16[start] - offset
        adj_char_start = start - char_offset

        for prefix, (md_type, idx) in MARKDOWN_TYPE_SEQUENCE:
            if not group.startswith(prefix):
                continue

            if md_type == "Quote":
                lines = []
                for line in group.split('\n'):
                    if line.startswith('> '):
                        lines.append(line[2:])
                    elif line.startswith('>'):
                        lines.append(line[1:])
                    else:
                        lines.append(line)
                raw_content = '\n'.join(lines)
                inner = to_metadata(raw_content)
                content = inner["text"]
                
                if "metadata" in inner:
                    for p in inner["metadata"]["meta_data_parts"]:
                        p["from_index"] += adj_start
                        parts.append(p)
                
            elif md_type == "Pre":
                raw = match.group(idx) or ""
                lines = raw.split('\n', 1)
                if len(lines) > 1 and lines[0].strip() and not lines[0].strip()[0].isalnum():
                    lang = lines[0].strip()
                    content = lines[1]
                else:
                    lang = ""
                    content = raw
                    
            elif md_type == "Link":
                content = match.group(idx) or ""
                url = match.group(9) or ""
                
            else:
                raw_content = match.group(idx) or ""
                inner = to_metadata(raw_content)
                content = inner["text"]
                if "metadata" in inner:
                    for p in inner["metadata"]["meta_data_parts"]:
                        p["from_index"] += adj_start
                        parts.append(p)

            content_len = len(content.encode("utf-16-be")) // 2
            markup_len = utf16[end] - utf16[start]
            char_markup = end - start

            if md_type == "Link" and url.startswith('u0'):
                part = {
                    "type": "MentionText",
                    "from_index": adj_start,
                    "length": content_len,
                    "mention_text_user_id": url
                }
            elif md_type == "Link":
                part = {
                    "type": "Link",
                    "from_index": adj_start,
                    "length": content_len,
                    "link_url": url
                }
            elif md_type == "Pre":
                part = {
                    "type": "Pre",
                    "from_index": adj_start,
                    "length": content_len,
                    "language": lang
                }
            elif md_type == "Quote":
                part = {
                    "type": "Quote",
                    "from_index": adj_start,
                    "length": content_len
                }
            else:
                part = {
                    "type": md_type,
                    "from_index": adj_start,
                    "length": content_len
                }

            if content_len > 0:
                parts.append(part)

            current = current[:adj_char_start] + content + current[end - char_offset:]
            offset += markup_len - content_len
            char_offset += char_markup - len(content)
            break

    result = {"text": current.strip()}
    if parts:
        result["metadata"] = {"meta_data_parts": parts}
    return result