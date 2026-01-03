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

    # Chinese sentence-ending punctuation set
    SENTENCE_END_PUNCTUATIONS_ZH = {
        "。",  # Chinese period
        "？",  # Chinese question mark
        "！",  # Chinese exclamation mark
        "；",  # Chinese semicolon
        "…",  # Ellipsis (single character)
        "……",  # Ellipsis (six dots)
    }

    # English sentence-ending punctuation set
    SENTENCE_END_PUNCTUATIONS_EN = {
        ".",  # English period
        "?",  # English question mark
        "!",  # English exclamation mark
        ";",  # English semicolon
        "…",  # Ellipsis (single character)
        "...",  # Ellipsis (three dots)
    }

    # Japanese sentence-ending punctuation set
    SENTENCE_END_PUNCTUATIONS_JA = {
        "。",  # Japanese period
        "？",  # Japanese question mark
        "！",  # Japanese exclamation mark
        "；",  # Japanese semicolon
        "……",  # Ellipsis (six dots)
    }

    # Korean sentence-ending punctuation set
    SENTENCE_END_PUNCTUATIONS_KO = {
        ".",  # English period (also used in Korean)
        "!",  # English exclamation mark
        "?",  # English question mark
        ";",  # English semicolon
        "。",  # Full-width period
        "！",  # Full-width exclamation mark
        "？",  # Full-width question mark
        "；",  # Full-width semicolon
        "…",  # Ellipsis (single character)
        "……",  # Ellipsis (six dots)
        "...",  # Ellipsis (three dots)
    }

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
        - Apostrophes (') in English contractions and possessives, e.g., "don't", "John's", "workers'"
        - Percent signs (%)
        - Hyphens/dashes (-)
        - Decimal points (.) when used in numbers, e.g., "99.5", "3.14", ".5"
        - Slashes (/) when used in dates, fractions, or units, e.g., "2024/01/01", "1/2", "km/h"

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
                # Preserve apostrophes in English contractions and possessives
                if i > 0 and i < len(text) - 1:
                    # Contractions: "don't"
                    if text[i - 1].isalpha() and text[i + 1].isalpha():
                        result.append(char)
                    # Possessives: "John's"
                    elif text[i - 1].isalpha() and text[i + 1] in "sS":
                        result.append(char)
                elif i > 0:
                    # Plural possessives: "workers'"
                    if text[i - 1].isalpha() and (i == len(text) - 1 or text[i + 1] in " \n\t"):
                        result.append(char)
            elif char == ".":
                # Preserve decimal points when used in numbers
                is_decimal = False
                if i > 0 and i < len(text) - 1:
                    # Both sides are digits (e.g., "99.5")
                    if text[i - 1].isdigit() and text[i + 1].isdigit():
                        is_decimal = True
                elif i > 0:
                    # Preceded by digit, followed by space or end (e.g., "5.")
                    if text[i - 1].isdigit():
                        if i == len(text) - 1 or text[i + 1] in " \n\t":
                            is_decimal = True
                elif i < len(text) - 1:
                    # Starts with decimal point, followed by digit (e.g., ".5")
                    if text[i + 1].isdigit():
                        is_decimal = True

                if is_decimal:
                    result.append(char)
            elif char == "/":
                # Preserve slashes in dates, fractions, or units (e.g., "2024/01/01", "1/2", "km/h")
                if i > 0 and i < len(text) - 1:
                    # Dates or fractions: digits on both sides (e.g., "2024/01/01", "1/2")
                    if text[i - 1].isdigit() and text[i + 1].isdigit():
                        result.append(char)
                    # Units: letters on both sides (e.g., "km/h", "m/s")
                    elif text[i - 1].isalpha() and text[i + 1].isalpha():
                        result.append(char)
            elif char in "%-":
                # Always preserve percent signs and hyphens
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
        - CJK Extension B: 0x20000-0x2A6DF
        - CJK Extension C: 0x2A700-0x2B73F
        - CJK Extension D: 0x2B740-0x2B81F
        - CJK Extension E: 0x2B820-0x2CEAF
        - CJK Extension F: 0x2CEB0-0x2EBEF
        - CJK Extension G: 0x30000-0x3134F
        - CJK Extension H: 0x31350-0x323AF
        - CJK Extension I: 0x2EBF0-0x2EE5F
        - CJK Compatibility Ideographs: 0xF900-0xFAFF
        - CJK Compatibility Ideographs Supplement: 0x2F800-0x2FA1F
        - Hiragana: 0x3040-0x309F
        - Katakana: 0x30A0-0x30FF
        - Hangul Syllables: 0xAC00-0xD7AF
        - Bopomofo (Zhuyin): 0x3100-0x312F

        Args:
            code_point: Unicode code point (integer).

        Returns:
            bool: True if the code point is a CJK character, False otherwise.
        """
        return (
            (0x4E00 <= code_point <= 0x9FFF)  # CJK Unified Ideographs
            or (0x3400 <= code_point <= 0x4DBF)  # CJK Extension A
            or (0x20000 <= code_point <= 0x2A6DF)  # CJK Extension B
            or (0x2A700 <= code_point <= 0x2B73F)  # CJK Extension C
            or (0x2B740 <= code_point <= 0x2B81F)  # CJK Extension D
            or (0x2B820 <= code_point <= 0x2CEAF)  # CJK Extension E
            or (0x2CEB0 <= code_point <= 0x2EBEF)  # CJK Extension F
            or (0x30000 <= code_point <= 0x3134F)  # CJK Extension G
            or (0x31350 <= code_point <= 0x323AF)  # CJK Extension H
            or (0x2EBF0 <= code_point <= 0x2EE5F)  # CJK Extension I
            or (0xF900 <= code_point <= 0xFAFF)  # CJK Compatibility Ideographs
            or (0x2F800 <= code_point <= 0x2FA1F)  # CJK Compatibility Ideographs Supplement
            or (0x3040 <= code_point <= 0x309F)  # Hiragana
            or (0x30A0 <= code_point <= 0x30FF)  # Katakana
            or (0xAC00 <= code_point <= 0xD7AF)  # Hangul Syllables
            or (0x3100 <= code_point <= 0x312F)  # Bopomofo (Zhuyin)
        )

    @staticmethod
    def _is_sentence_end_with_zh_punctuation(text: str) -> bool:
        """
        Check if text ends with Chinese sentence-ending punctuation (private method).

        Supported sentence-ending punctuation:
        - Period: 。
        - Question mark: ？
        - Exclamation mark: ！
        - Semicolon: ；
        - Ellipsis: … (single character), …… (six dots)

        Args:
            text: Text to check (can be a single character or multiple characters, e.g., "段。")

        Returns:
            bool: True if text ends with sentence-ending punctuation, False otherwise.
        """
        if not text:
            return False

        # Check if text ends with any sentence-ending punctuation
        for punct in UniText.SENTENCE_END_PUNCTUATIONS_ZH:
            if text.endswith(punct):
                return True
        return False

    @staticmethod
    def _is_sentence_end_with_en_punctuation(text: str) -> bool:
        """
        Check if text ends with English sentence-ending punctuation (private method).

        Supported sentence-ending punctuation:
        - Period: .
        - Question mark: ?
        - Exclamation mark: !
        - Semicolon: ;
        - Ellipsis: … (single character), ... (three dots)

        Args:
            text: Text to check (can be a single character or multiple characters, e.g., "end.")

        Returns:
            bool: True if text ends with sentence-ending punctuation, False otherwise.
        """
        if not text:
            return False

        # Check if text ends with any sentence-ending punctuation
        for punct in UniText.SENTENCE_END_PUNCTUATIONS_EN:
            if text.endswith(punct):
                return True
        return False

    @staticmethod
    def _is_sentence_end_with_ja_punctuation(text: str) -> bool:
        """
        Check if text ends with Japanese sentence-ending punctuation (private method).

        Supported sentence-ending punctuation:
        - Period: 。
        - Question mark: ？
        - Exclamation mark: ！
        - Semicolon: ；
        - Ellipsis: …… (six dots)

        Args:
            text: Text to check (can be a single character or multiple characters, e.g., "終わり。")

        Returns:
            bool: True if text ends with sentence-ending punctuation, False otherwise.
        """
        if not text:
            return False

        # Check if text ends with any sentence-ending punctuation
        for punct in UniText.SENTENCE_END_PUNCTUATIONS_JA:
            if text.endswith(punct):
                return True
        return False

    @staticmethod
    def _is_sentence_end_with_ko_punctuation(text: str) -> bool:
        """
        Check if text ends with Korean sentence-ending punctuation (private method).

        Supported sentence-ending punctuation:
        - Half-width period: .
        - Half-width question mark: ?
        - Half-width exclamation mark: !
        - Half-width semicolon: ;
        - Full-width period: 。
        - Full-width question mark: ？
        - Full-width exclamation mark: ！
        - Full-width semicolon: ；
        - Ellipsis: … (single character), …… (six dots), ... (three dots)

        Args:
            text: Text to check (can be a single character or multiple characters, e.g., "끝.")

        Returns:
            bool: True if text ends with sentence-ending punctuation, False otherwise.
        """
        if not text:
            return False

        # Check if text ends with any sentence-ending punctuation
        for punct in UniText.SENTENCE_END_PUNCTUATIONS_KO:
            if text.endswith(punct):
                return True
        return False

    @staticmethod
    def is_sentence_end_with_punctuation(text: str, lang: str) -> bool:
        """
        Check if text ends with sentence-ending punctuation (based on language type).

        Calls the corresponding private method based on the specified language type.
        Supported language types: 'zh' (Chinese), 'en' (English), 'ja' (Japanese), 'ko' (Korean).

        Can be used to check if a Word's word field (e.g., "段。", "end.") ends with
        sentence-ending punctuation.

        Args:
            text: Text to check (can be a single character or multiple characters, e.g., "段。", "end.")
            lang: Language type, supports 'zh', 'en', 'ja', 'ko'

        Returns:
            bool: True if text ends with sentence-ending punctuation, False otherwise.

        Raises:
            ValueError: If lang parameter is not a supported language type.
        """
        if not text:
            return False

        lang = lang.lower()
        if lang == "zh":
            return UniText._is_sentence_end_with_zh_punctuation(text)
        elif lang == "en":
            return UniText._is_sentence_end_with_en_punctuation(text)
        elif lang == "ja":
            return UniText._is_sentence_end_with_ja_punctuation(text)
        elif lang == "ko":
            return UniText._is_sentence_end_with_ko_punctuation(text)
        else:
            raise ValueError(f"Unsupported language: {lang}. Supported languages: 'zh', 'en', 'ja', 'ko'")
