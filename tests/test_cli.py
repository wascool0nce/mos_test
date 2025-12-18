import io
import json
import unittest
from unittest.mock import patch

from src.domain.okved import Okved
from src.usecases.find_okved import MatchResult
from src.presentation import cli


class CliTest(unittest.TestCase):
    def test_cli_outputs_json(self) -> None:
        fake_result = MatchResult(
            normalized_phone="+79991112233",
            okved=Okved(code="01", name="One"),
            match_length=2,
            fallback_used=False,
        )
        with patch.object(cli.FindOkvedUseCase, "execute", return_value=fake_result):
            stdout = io.StringIO()
            with patch("sys.stdout", stdout):
                exit_code = cli.main(["+7 999 111 22 33"])
        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("+79991112233", payload["normalized_phone"])
        self.assertEqual("01", payload["okved_code"])
        self.assertFalse(payload["fallback_used"])


if __name__ == "__main__":
    unittest.main()
