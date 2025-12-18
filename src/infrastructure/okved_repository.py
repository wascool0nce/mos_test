"""
Инфраструктурный слой для загрузки ОКВЭД по HTTPS.
"""

import json
from typing import Callable, Iterable, List
from urllib.error import URLError
from urllib.request import urlopen

from src.domain.okved import Okved, flatten_okved_tree

DEFAULT_OKVED_URL = "https://raw.githubusercontent.com/bergstar/testcase/master/okved.json"


class OkvedRepository:
    """Загружает и парсит данные ОКВЭД из удалённого JSON."""

    def __init__(self, opener: Callable[[str], Iterable[bytes]] = urlopen):
        """Инициализирует репозиторий.

        Args:
            opener: Совместимая с urllib.request.urlopen функция (удобно мокать).
        """
        self._opener = opener

    def fetch(self, url: str = DEFAULT_OKVED_URL) -> List[Okved]:
        """Загружает дерево ОКВЭД по HTTPS и разворачивает его."""
        try:
            with self._opener(url) as response:
                payload = json.load(response)
        except URLError as exc:
            raise ConnectionError(f"Не удалось загрузить OKVED: {exc}") from exc
        return flatten_okved_tree(payload)
