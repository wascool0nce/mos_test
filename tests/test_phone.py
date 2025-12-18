import unittest

from src.domain.phone import NormalizationError, PhoneNormalizer


class PhoneNormalizerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.normalizer = PhoneNormalizer()

    def test_normalizes_11_digit_input(self) -> None:
        result = self.normalizer.normalize("+7 (999) 123-45-67")
        self.assertTrue(result.is_success)
        self.assertEqual("+79991234567", result.value)

    def test_normalizes_domestic_format(self) -> None:
        result = self.normalizer.normalize("8 999 1112233")
        self.assertTrue(result.is_success)
        self.assertEqual("+79991112233", result.value)

    def test_rejects_non_mobile_number(self) -> None:
        result = self.normalizer.normalize("8 123 456 78 90")
        self.assertFalse(result.is_success)
        self.assertEqual("Ожидается мобильный номер, начинающийся с 9.", result.error)

    def test_rejects_invalid_length(self) -> None:
        result = self.normalizer.normalize("12345")
        self.assertFalse(result.is_success)
        self.assertEqual("Не удалось нормализовать номер.", result.error)

    def test_raises_on_non_string(self) -> None:
        with self.assertRaises(NormalizationError):
            self.normalizer.normalize(79991234567)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
