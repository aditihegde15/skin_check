from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass(frozen=True)
class IngredientInfo:
    tags: List[str]
    severity: int  
    note: str

INGREDIENT_DB: Dict[str, IngredientInfo] = {
    "fragrance": IngredientInfo(
        ["fragrance", "irritant"], 4,
        "Fragrance can irritate sensitive skin."
    ),
    "parfum": IngredientInfo(
        ["fragrance", "irritant"], 4,
        "Parfum is the same as fragrance."
    ),
    "denatured alcohol": IngredientInfo(
        ["drying", "irritant"], 3,
        "Can be drying for some skin types."
    ),
    "alcohol denat": IngredientInfo(
        ["drying", "irritant"], 3,
        "Can be drying for some skin types."
    ),
    "limonene": IngredientInfo(
        ["allergen", "fragrance"], 3,
        "Common fragrance allergen."
    ),
    "linalool": IngredientInfo(
        ["allergen", "fragrance"], 3,
        "Common fragrance allergen."
    ),
    "niacinamide": IngredientInfo(
        ["beneficial"], 0,
        "Supports skin barrier and tone."
    ),
    "glycerin": IngredientInfo(
        ["beneficial"], 0,
        "Hydrating."
    ),
}

def lookup(ingredient: str) -> Optional[IngredientInfo]:
    if not ingredient:
        return None

    key = ingredient.lower().strip()
    return INGREDIENT_DB.get(key)

