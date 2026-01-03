# uni-text

A lightweight Python library for Unicode text processing, including punctuation detection, punctuation removal, and CJK character detection.

## Features

- **Simple API**: Static methods for all text processing operations
- **Punctuation handling**: Detect and remove punctuation marks with customizable rules
- **CJK support**: Detect Chinese, Japanese, and Korean characters
- **Unicode-based**: Uses Unicode categories for accurate character classification
- **Zero dependencies**: Uses only Python standard library (`unicodedata`)
- **Type safety**: Full type hints for better IDE support

## Installation

```bash
pip install uni-text
```

## Quick Start

### Check if a character is punctuation

```python
from uni_text import UniText

# Check if a character is punctuation
is_punc = UniText.is_punctuation(",")  # True
is_punc = UniText.is_punctuation("a")  # False
```

### Remove punctuation from text

```python
from uni_text import UniText

# Remove punctuation (preserves apostrophes in contractions, %, and -)
text = "Hello, world! Don't worry."
cleaned = UniText.remove_punctuations(text)
# Result: "Hello world Don't worry"
```

### Remove punctuation in Chinese context

```python
from uni_text import UniText

# Remove punctuation (also preserves decimal points)
text = "价格是 99.5 元，很便宜。"
cleaned = UniText.remove_punctuations_in_zh(text)
# Result: "价格是 99.5 元很便宜"
```

### Remove consecutive punctuation

```python
from uni_text import UniText

# Remove consecutive punctuation marks, keeping only the first
text = "你好，，，世界"
cleaned = UniText.remove_consecutive_punctuations(text)
# Result: "你好，世界"
```

### Check if a code point is CJK character

```python
from uni_text import UniText

# Check if a Unicode code point is a CJK character
code_point = ord("中")
is_cjk = UniText.is_cjk_character(code_point)  # True

code_point = ord("A")
is_cjk = UniText.is_cjk_character(code_point)  # False
```

## API Reference

### UniText

Main utility class for Unicode text processing. All methods are static.

#### `UniText.is_punctuation(char)`

Check if a character is a punctuation mark.

**Parameters:**

- `char` (str): Character to check (must be a single character).

**Returns:**

- bool: `True` if the character is punctuation, `False` otherwise.

**Example:**

```python
from uni_text import UniText

is_punc = UniText.is_punctuation(",")  # True
is_punc = UniText.is_punctuation("a")  # False
```

#### `UniText.remove_punctuations(text)`

Remove punctuation marks from text.

Uses Unicode category to remove punctuation, but preserves the following special cases:

- Apostrophes (`'`) in English contractions, e.g., "don't"
- Percent signs (`%`)
- Hyphens/dashes (`-`)

**Parameters:**

- `text` (str): Original text (may contain punctuation).

**Returns:**

- str: Text with punctuation removed (special characters preserved).

**Example:**

```python
from uni_text import UniText

text = "Hello, world! Don't worry - it's 100% safe."
cleaned = UniText.remove_punctuations(text)
# Result: "Hello world Don't worry - it's 100% safe"
```

#### `UniText.remove_punctuations_in_zh(text)`

Remove punctuation marks from text (Chinese context).

Similar to `remove_punctuations()`, but also preserves decimal points (`.`) in addition to the other special characters.

**Parameters:**

- `text` (str): Original text (may contain punctuation).

**Returns:**

- str: Text with punctuation removed (special characters preserved).

**Example:**

```python
from uni_text import UniText

text = "价格是 99.5 元，很便宜。"
cleaned = UniText.remove_punctuations_in_zh(text)
# Result: "价格是 99.5 元很便宜"
```

#### `UniText.remove_consecutive_punctuations(text)`

Remove consecutive punctuation marks, keeping only the first one.

When consecutive punctuation marks are encountered (regardless of whether they are the same), only the first one is kept, and all subsequent consecutive punctuation marks are removed.

**Parameters:**

- `text` (str): Original text (may contain repeated punctuation).

**Returns:**

- str: Text with consecutive punctuation removed.

**Examples:**

```python
from uni_text import UniText

# Same punctuation repeated
text = "你好，，，世界"
cleaned = UniText.remove_consecutive_punctuations(text)
# Result: "你好，世界"

# Different punctuation marks
text = "测试！？。结束"
cleaned = UniText.remove_consecutive_punctuations(text)
# Result: "测试！结束"
```

#### `UniText.is_cjk_character(code_point)`

Check if a Unicode code point is a CJK character.

CJK character ranges include:

- CJK Unified Ideographs: 0x4E00-0x9FFF
- CJK Extension A: 0x3400-0x4DBF
- CJK Compatibility Ideographs: 0xF900-0xFAFF
- Hiragana: 0x3040-0x309F
- Katakana: 0x30A0-0x30FF
- Hangul Syllables: 0xAC00-0xD7AF

**Parameters:**

- `code_point` (int): Unicode code point (integer).

**Returns:**

- bool: `True` if the code point is a CJK character, `False` otherwise.

**Example:**

```python
from uni_text import UniText

# Chinese character
code_point = ord("中")
is_cjk = UniText.is_cjk_character(code_point)  # True

# Japanese hiragana
code_point = ord("あ")
is_cjk = UniText.is_cjk_character(code_point)  # True

# Korean character
code_point = ord("한")
is_cjk = UniText.is_cjk_character(code_point)  # True

# Latin character
code_point = ord("A")
is_cjk = UniText.is_cjk_character(code_point)  # False
```

## Requirements

- Python >= 3.10

No external dependencies required. This package uses only Python standard library modules (`unicodedata`).

## License

MIT License
