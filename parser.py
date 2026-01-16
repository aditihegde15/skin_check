import re
from typing import List

_SPLIT_RE = re.compile(r",|;|\n|\t")
_PARENS_RE = re.compile(r"\([^)]*\)")

def normalize_ingredient(text: str) -> str:
    t = text.strip().lower()
    t = re.sub(r"\s+", " ", t)
    t = t.replace("/", " / ")
    t = re.sub(r"\s+", " ", t).strip()
    return t

def parse_ingredients(raw: str) -> List[str]:
    if not raw or not raw.strip():
        return []

    no_parens = _PARENS_RE.sub("", raw)
    parts = [p.strip() for p in _SPLIT_RE.split(no_parens) if p.strip()]
    normalized = [normalize_ingredient(p) for p in parts]

    seen = set()
    out = []
    for ing in normalized:
        if ing and ing not in seen:
            out.append(ing)
            seen.add(ing)

    return out
