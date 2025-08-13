from typing import Optional, Tuple
from .config import settings

def resolve_table(user_text: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract a table name from user text and map to ID via TABLE_MAP.
    Returns (table_name, table_id) or (None, None)."""

    if not user_text:
        return None, None
    t = user_text.strip()
    lowers = t.lower()
    # Try explicit keywords
    candidates = []
    for kw in ("table:", "ตาราง:", "table ", "ตาราง "):
        if kw in lowers:
            idx = lowers.index(kw) + len(kw)
            seg = t[idx:].strip()
            if seg:
                candidates.append(seg.split()[0].strip("：:，,.;"))

    # Fallback: scan known map keys
    for name in settings.TABLE_MAP.keys():
        if name.lower() in lowers:
            candidates.append(name)

    # Normalize against map
    for cand in candidates:
        for k, v in settings.TABLE_MAP.items():
            if k.lower() == cand.lower():
                if _table_allowed(v):
                    return k, v
                else:
                    return k, None
    return None, None

def _table_allowed(table_id: str) -> bool:
    if not settings.ALLOWED_TABLE_IDS:
        return True
    return table_id in settings.ALLOWED_TABLE_IDS
