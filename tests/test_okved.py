import unittest

from src.domain.okved import Okved, flatten_okved_tree


class OkvedDomainTest(unittest.TestCase):
    def test_numeric_code_extraction(self) -> None:
        okved = Okved(code="01.11.1", name="Test")
        self.assertEqual("01111", okved.numeric_code)

    def test_flatten_okved_tree(self) -> None:
        tree = [
            {"code": "01", "name": "Root", "items": [{"code": "01.1", "name": "Child"}]},
            {"code": "02", "name": "Second"},
        ]
        flattened = flatten_okved_tree(tree)
        self.assertEqual(3, len(flattened))
        self.assertEqual("01", flattened[0].code)
        self.assertEqual("Child", flattened[1].name)
        self.assertEqual("02", flattened[2].code)


if __name__ == "__main__":
    unittest.main()
