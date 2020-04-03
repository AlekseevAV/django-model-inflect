import logging
from typing import Dict, Iterable

import pymorphy2

from .utils import Singleton


logger = logging.getLogger(__name__)


class Inflector(metaclass=Singleton):
    def __init__(self) -> None:
        self._morph = pymorphy2.MorphAnalyzer()

    def inflect_to_case(self, string_to_inflect: str, case: str) -> str:
        """Inflect all words in string to case"""
        inflected_words = []
        words_to_inflect = str(string_to_inflect).split()
        for word in words_to_inflect:
            inflected_words.append(self._safe_inflect(word, case))
        return ' '.join(inflected_words)

    def inflect_to_cases(self, string_to_inflect: str, cases: Iterable[str]) -> Dict[str, str]:
        """Inflect all words in string to multiple cases"""
        result = dict()
        for case in cases:
            result[case] = self.inflect_to_case(string_to_inflect, case)
        return result

    def _safe_inflect(self, string: str, case: str) -> str:
        is_capitalized_string = string[0].isupper()
        try:
            # .inflect() can return None and None.word will raise AttributeError
            string = self._morph.parse(string)[0].inflect({case}).word
        except AttributeError:
            logger.warning('Cannot inflect word: {} to {} case.'.format(string, case))
        if is_capitalized_string:
            string = string.capitalize()
        return string
