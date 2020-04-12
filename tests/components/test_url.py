#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from typing import Any, Dict, List
from unittest import mock

import pytest
from urlextract import URLExtract

from rasam import URLEntityExtractor


def test_init() -> None:
    extractor = URLEntityExtractor()
    assert isinstance(extractor.extractor, URLExtract)


@pytest.mark.parametrize(
    "text, expected",
    ids=["no_url", "has_url", "has_multiple_urls"],
    argvalues=[
        ("goto google", []),
        (
            "goto google.com",
            [
                {
                    "start": 5,
                    "end": 15,
                    "value": "google.com",
                    "entity": "URL",
                    "extractor": "URLEntityExtractor",
                    "confidence": 1.0,
                }
            ],
        ),
        (
            "goto google.com facebook.com",
            [
                {
                    "start": 5,
                    "end": 15,
                    "value": "google.com",
                    "entity": "URL",
                    "extractor": "URLEntityExtractor",
                    "confidence": 1.0,
                },
                {
                    "start": 16,
                    "end": 28,
                    "value": "facebook.com",
                    "entity": "URL",
                    "extractor": "URLEntityExtractor",
                    "confidence": 1.0,
                },
            ],
        ),
    ],
)
def test_process(text: str, expected: List[Dict[str, Any]]) -> None:
    message = mock.MagicMock()
    message.text = text
    message.get.return_value = []

    extractor = URLEntityExtractor()
    extractor.process(message)
    message.set.assert_called_once_with("entities", expected, add_to_output=True)
