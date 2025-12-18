"""
CLI для игры «Найди свой ОКВЭД по номеру телефона».
"""

import argparse
import json
import sys
from typing import Any, Dict

from src.domain.phone import PhoneNormalizer
from src.infrastructure.okved_repository import OkvedRepository
from src.usecases.find_okved import FindOkvedUseCase, OkvedMatcher


def build_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов CLI."""
    parser = argparse.ArgumentParser(description="Найди свой ОКВЭД по номеру телефона.")
    parser.add_argument("phone", help="Номер телефона в любом формате.")
    parser.add_argument(
        "--okved-url",
        default=None,
        help="Переопределить URL для загрузки okved.json (по умолчанию GitHub).",
    )
    return parser


def format_result(result: Any) -> str:
    """Готовит JSON-строку для вывода CLI."""
    output: Dict[str, Any] = {
        "normalized_phone": result.normalized_phone,
        "okved_code": result.okved.code,
        "okved_name": result.okved.name,
        "match_length": result.match_length,
        "fallback_used": result.fallback_used,
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def main(argv: list[str] | None = None) -> int:
    """Точка входа CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    use_case = FindOkvedUseCase(OkvedRepository(), PhoneNormalizer(), OkvedMatcher())
    try:
        result = use_case.execute(args.phone, args.okved_url)
    except Exception as exc:  # pragma: no cover - defensive CLI handling
        parser.error(str(exc))
        return 2

    print(format_result(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
