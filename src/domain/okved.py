"""
Доменные модели для ОКВЭД и вспомогательные функции сопоставления.
"""

import re
from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class Okved:
    """Плоская запись ОКВЭД."""

    code: str
    name: str

    @property
    def numeric_code(self) -> str:
        """Возвращает только цифры из кода ОКВЭД."""
        return re.sub(r"\D", "", self.code)


def flatten_okved_tree(tree: Iterable[dict]) -> List["Okved"]:
    """Разворачивает вложенный JSON ОКВЭД в список Okved."""
    items: List[Okved] = []
    for node in tree:
        items.append(Okved(code=node["code"], name=node["name"]))
        nested = node.get("items") or []
        items.extend(flatten_okved_tree(nested))
    return items
