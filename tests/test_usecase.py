import unittest

from src.domain.okved import Okved
from src.domain.phone import PhoneNormalizer
from src.usecases.find_okved import FindOkvedUseCase, MatchResult, OkvedMatcher


class StubRepository:
    def __init__(self, okved_list: list[Okved]):
        self._data = okved_list
        self.used_url: str | None = None

    def fetch(self, url: str | None = None) -> list[Okved]:
        self.used_url = url
        return self._data


class UseCaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.okveds = [
            Okved(code="01", name="One"),
            Okved(code="011", name="Longer"),
            Okved(code="02", name="Two"),
        ]
        self.repository = StubRepository(self.okveds)
        self.use_case = FindOkvedUseCase(self.repository, PhoneNormalizer(), OkvedMatcher())

    def test_selects_longest_suffix_match(self) -> None:
        result: MatchResult = self.use_case.execute("8 (999) 999-0011")
        self.assertEqual("+79999990011", result.normalized_phone)
        self.assertEqual("011", result.okved.code)
        self.assertEqual(3, result.match_length)
        self.assertFalse(result.fallback_used)

    def test_uses_fallback_when_no_match(self) -> None:
        result: MatchResult = self.use_case.execute("+7 912 345 6789")
        self.assertTrue(result.fallback_used)
        self.assertEqual(0, result.match_length)
        self.assertIn(result.okved, self.okveds)

    def test_passes_custom_url(self) -> None:
        self.use_case.execute("+7 999 000 0000", okved_url="https://example.com/data.json")
        self.assertEqual("https://example.com/data.json", self.repository.used_url)

    def test_raises_on_invalid_phone(self) -> None:
        with self.assertRaises(ValueError):
            self.use_case.execute("12345")


class MatcherFallbackTest(unittest.TestCase):
    def test_fallback_requires_candidates(self) -> None:
        matcher = OkvedMatcher()
        with self.assertRaises(ValueError):
            matcher._fallback("79990001122", [])


if __name__ == "__main__":
    unittest.main()
