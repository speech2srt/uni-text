"""
Unicode Text Processing Module

Provides utilities for text processing, including punctuation detection,
punctuation removal, and CJK character detection.
"""

import logging
import unicodedata

logger = logging.getLogger(__name__)


class UniText:
    """
    Utility class for Unicode text processing.

    All methods are static and provide a simple interface for working with
    text data, including punctuation handling and CJK character detection.
    """

    @staticmethod
    def is_punctuation(char: str) -> bool:
        """
        Check if a character is a punctuation mark.

        Uses Unicode category to determine punctuation. All categories starting
        with "P" are considered punctuation.

        Args:
            char: Character to check.

        Returns:
            bool: True if the character is punctuation, False otherwise.
        """
        if not char or len(char) != 1:
            return False
        return unicodedata.category(char).startswith("P")

    @staticmethod
    def remove_punctuations(text: str) -> str:
        """
        Remove punctuation marks from text.

        Uses Unicode category to remove punctuation, but preserves the following
        special cases:
        - Apostrophes (') in English contractions, e.g., "don't"
        - Percent signs (%)
        - Hyphens/dashes (-)

        Args:
            text: Original text (may contain punctuation).

        Returns:
            str: Text with punctuation removed (special characters preserved).
        """
        if not text:
            return text

        result = []
        for i, char in enumerate(text):
            if not UniText.is_punctuation(char):
                result.append(char)
            elif char == "'":
                # Preserve apostrophes in English contractions
                if i > 0 and i < len(text) - 1:
                    if text[i - 1].isalpha() and text[i + 1].isalpha():
                        result.append(char)
            elif char in "%-":
                # Always preserve percent signs and hyphens
                result.append(char)

        return "".join(result)

    @staticmethod
    def remove_punctuations_in_zh(text: str) -> str:
        """
        Remove punctuation marks from text (Chinese context).

        Uses Unicode category to remove punctuation, but preserves the following
        special cases:
        - Apostrophes (') in English contractions, e.g., "don't"
        - Percent signs (%)
        - Hyphens/dashes (-)
        - Decimal points (.)

        Args:
            text: Original text (may contain punctuation).

        Returns:
            str: Text with punctuation removed (special characters preserved).
        """
        if not text:
            return text

        result = []
        for i, char in enumerate(text):
            if not UniText.is_punctuation(char):
                result.append(char)
            elif char == "'":
                # Preserve apostrophes in English contractions
                if i > 0 and i < len(text) - 1:
                    if text[i - 1].isalpha() and text[i + 1].isalpha():
                        result.append(char)
            elif char in "%-.":
                # Always preserve percent signs, hyphens, and decimal points
                result.append(char)

        return "".join(result)

    @staticmethod
    def remove_consecutive_punctuations(text: str) -> str:
        """
        Remove consecutive punctuation marks, keeping only the first one.

        Uses `is_punctuation()` to detect punctuation. When consecutive punctuation
        marks are encountered (regardless of whether they are the same), only the
        first one is kept, and all subsequent consecutive punctuation marks are removed.

        Examples:
            "你好，，，世界" -> "你好，世界"
            "这是。。。测试" -> "这是。测试"
            "多个！！！感叹号" -> "多个！感叹号"
            "混合，。，。标点" -> "混合，标点" (keep first punctuation, remove subsequent consecutive punctuation)
            "测试！？。结束" -> "测试！结束" (keep first punctuation, remove subsequent consecutive punctuation)

        Args:
            text: Original text (may contain repeated punctuation).

        Returns:
            str: Text with consecutive punctuation removed.
        """
        if not text:
            return text

        result = []
        prev_is_punc = False

        for char in text:
            is_punc = UniText.is_punctuation(char)

            # If current character is punctuation and previous character is also punctuation, skip (regardless of whether they are the same)
            if is_punc and prev_is_punc:
                continue

            # Otherwise add to result
            result.append(char)
            prev_is_punc = is_punc

        return "".join(result)

    @staticmethod
    def is_cjk_character(code_point: int) -> bool:
        """
        Check if a Unicode code point is a CJK character.

        CJK character ranges include:
        - CJK Unified Ideographs: 0x4E00-0x9FFF
        - CJK Extension A: 0x3400-0x4DBF
        - CJK Compatibility Ideographs: 0xF900-0xFAFF
        - Hiragana: 0x3040-0x309F
        - Katakana: 0x30A0-0x30FF
        - Hangul Syllables: 0xAC00-0xD7AF

        Args:
            code_point: Unicode code point (integer).

        Returns:
            bool: True if the code point is a CJK character, False otherwise.
        """
        return (
            (0x4E00 <= code_point <= 0x9FFF)  # CJK Unified Ideographs
            or (0x3400 <= code_point <= 0x4DBF)  # CJK Extension A
            or (0xF900 <= code_point <= 0xFAFF)  # CJK Compatibility Ideographs
            or (0x3040 <= code_point <= 0x309F)  # Hiragana
            or (0x30A0 <= code_point <= 0x30FF)  # Katakana
            or (0xAC00 <= code_point <= 0xD7AF)  # Hangul Syllables
        )
