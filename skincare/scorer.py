from dataclasses import dataclass
from typing import Dict, List, Optional

from .database import lookup

@dataclass
class Finding:
    ingredient: str
    tags: List[str]
    severity: int
    note: str

@dataclass
class Report:
    verdict: str
    score: int
    findings: List[Finding]
    summary: Dict[str, int]

def _verdict_from_score(score: int) -> str:
    if score >= 80:
        return "Safe"
    if score >= 55:
        return "Caution"
    return "Avoid"

def analyze(ingredients: List[str], skin_focus: Optional[str] = None) -> Report:
    findings: List[Finding] = []
    tag_counts: Dict[str, int] = {}
    penalty = 0

    for ing in ingredients:
        info = lookup(ing)
        if not info:
            continue

        if info.severity > 0:
            weight = 1.0
            if skin_focus == "sensitive" and ("irritant" in info.tags or "allergen" in info.tags):
                weight = 1.25
            if skin_focus == "acne_prone" and "comedogenic" in info.tags:
                weight = 1.25

            penalty += int(info.severity * 6 * weight)

        for t in info.tags:
            tag_counts[t] = tag_counts.get(t, 0) + 1

        findings.append(Finding(
            ingredient=ing,
            tags=info.tags,
            severity=info.severity,
            note=info.note
        ))

    score = max(0, min(100, 100 - penalty))
    verdict = _verdict_from_score(score)

    findings.sort(key=lambda f: f.severity, reverse=True)

    return Report(
        verdict=verdict,
        score=score,
        findings=findings,
        summary=tag_counts
    )
