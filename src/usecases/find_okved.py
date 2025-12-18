"""
Прикладной сценарий поиска кода ОКВЭД по номеру телефона.
"""

import re
from dataclasses import dataclass
from typing import Iterable, List

from src.domain.okved import Okved
from src.domain.phone import NormalizationResult, PhoneNormalizer
from src.infrastructure.okved_repository import OkvedRepository


@dataclass(frozen=True)
class MatchResult:
    """Результат сопоставления с ОКВЭД."""

    normalized_phone: str
    okved: Okved
    match_length: int
    fallback_used: bool


class OkvedMatcher:
    """Выбирает код ОКВЭД с максимальным совпадением по окончанию номера."""

    def find(self, normalized_phone: str, okved_list: Iterable[Okved]) -> MatchResult:
        """Находит лучшее совпадение или применяет резервную стратегию."""
        phone_digits = re.sub(r"\D", "", normalized_phone)
        candidates: List[Okved] = [item for item in okved_list if item.numeric_code]
        best = self._find_best_match(phone_digits, candidates)
        if best:
            return MatchResult(
                normalized_phone=normalized_phone,
                okved=best,
                match_length=len(best.numeric_code),
                fallback_used=False,
            )
        fallback = self._fallback(phone_digits, candidates)
        return MatchResult(
            normalized_phone=normalized_phone,
            okved=fallback,
            match_length=0,
            fallback_used=True,
        )

    def _find_best_match(self, phone_digits: str, candidates: List[Okved]) -> Okved | None:
        best: Okved | None = None
        best_length = -1
        for item in candidates:
            code_digits = item.numeric_code
            if phone_digits.endswith(code_digits) and len(code_digits) > best_length:
                best = item
                best_length = len(code_digits)
        return best

    def _fallback(self, phone_digits: str, candidates: List[Okved]) -> Okved:
        """Детерминированный резервный выбор на основе суммы цифр."""
        if not candidates:
            raise ValueError("Список ОКВЭД пуст.")
        digit_sum = sum(int(d) for d in phone_digits) or 1
        index = digit_sum % len(candidates)
        return candidates[index]


class FindOkvedUseCase:
    """Оркестрирует нормализацию, загрузку ОКВЭД и сопоставление."""

    def __init__(
        self,
        repository: OkvedRepository,
        normalizer: PhoneNormalizer,
        matcher: OkvedMatcher,
    ):
        self._repository = repository
        self._normalizer = normalizer
        self._matcher = matcher

    def execute(self, raw_phone: str, okved_url: str | None = None) -> MatchResult:
        """Выполняет сценарий нормализации и поиска подходящего ОКВЭД."""
        normalization: NormalizationResult = self._normalizer.normalize(raw_phone)
        if not normalization.is_success:
            raise ValueError(normalization.error or "Неизвестная ошибка нормализации.")
        okved_list = self._repository.fetch(okved_url) if okved_url else self._repository.fetch()
        return self._matcher.find(normalization.value, okved_list)
