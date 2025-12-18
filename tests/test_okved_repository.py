import io
import json
import unittest
from urllib.error import URLError

from src.infrastructure.okved_repository import OkvedRepository


class FakeResponse:
    def __init__(self, payload: list[dict]):
        self._stream = io.StringIO(json.dumps(payload))

    def __enter__(self):
        return self._stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stream.close()
        return False


class OkvedRepositoryTest(unittest.TestCase):
    def test_fetch_parses_json(self) -> None:
        payload = [{"code": "01", "name": "Test"}]
        repository = OkvedRepository(opener=lambda url: FakeResponse(payload))
        result = repository.fetch("http://example.com/okved.json")
        self.assertEqual(1, len(result))
        self.assertEqual("01", result[0].code)

    def test_fetch_raises_on_network_error(self) -> None:
        repository = OkvedRepository(opener=lambda url: (_ for _ in ()).throw(URLError("boom")))
        with self.assertRaises(ConnectionError):
            repository.fetch("http://invalid")


if __name__ == "__main__":
    unittest.main()
