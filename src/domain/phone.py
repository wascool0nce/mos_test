"""
Доменные сервисы для нормализации телефонных номеров.

По всему проекту используются докстринги в стиле Google.
"""

import re
from dataclasses import dataclass
from typing import Optional


class NormalizationError(Exception):
    """Ошибка при невозможности нормализовать номер."""


@dataclass(frozen=True)
class NormalizationResult:
    """Результат нормализации номера."""

    value: Optional[str]
    error: Optional[str]

    @property
    def is_success(self) -> bool:
        """Возвращает True, если нормализация прошла успешно."""
        return self.value is not None


class PhoneNormalizer:
    """Нормализует мобильные номера РФ в формат +79XXXXXXXXX."""

    REQUIRED_LENGTH = 10
    COUNTRY_PREFIX = "+7"

    def normalize(self, raw: str) -> NormalizationResult:
        """Приводит ввод к +79XXXXXXXXX или возвращает ошибку.

        Args:
            raw: Произвольный ввод, содержащий российский мобильный номер.

        Returns:
            NormalizationResult с нормализованным номером или текстом ошибки.

        Raises:
            NormalizationError: Если вход не является строкой.
        """
        if not isinstance(raw, str):
            raise NormalizationError("Номер телефона должен быть строкой.")

        digits = "".join(re.findall(r"\d", raw))
        if not digits:
            return NormalizationResult(None, "В номере отсутствуют цифры.")

        candidate = self._normalize_digits(digits)
        if candidate is None:
            return NormalizationResult(None, "Не удалось нормализовать номер.")

        if candidate[0] != "9":
            return NormalizationResult(None, "Ожидается мобильный номер, начинающийся с 9.")

        return NormalizationResult(f"{self.COUNTRY_PREFIX}{candidate}", None)

    def _normalize_digits(self, digits: str) -> Optional[str]:
        """Преобразует цифры в 10-значный формат или возвращает None."""
        if len(digits) == 11 and digits[0] in ("7", "8"):
            return digits[1:]
        if len(digits) == 10 and digits[0] == "9":
            return digits
        return None
