"""
Uni Text - A Python library for Unicode text processing.

This package provides utilities for:
- Punctuation detection and removal
- CJK character detection
- Text normalization and cleaning
"""

import logging

from .uni_text import UniText

__version__ = "0.3.0"

# Configure library root logger
# Use NullHandler to ensure library remains silent when user hasn't configured logging
# If user configures logging (e.g., logging.basicConfig()), logs will bubble up to root logger for processing
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__ = [
    "UniText",
]
