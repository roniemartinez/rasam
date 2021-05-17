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
    [
        pytest.param("goto google", [], id="no-url"),
        pytest.param(
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
            id="has-url",
        ),
        pytest.param(
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
            id="has-multiple-urls",
        ),
    ],
)
def test_process(text: str, expected: List[Dict[str, Any]]) -> None:
    message = mock.MagicMock()
    message.data = {"text": text}
    message.get.return_value = []

    extractor = URLEntityExtractor()
    extractor.process(message)
    message.set.assert_called_once_with("entities", expected, add_to_output=True)
