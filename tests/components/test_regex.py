#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import os
import re
from typing import Any, Dict, List
from unittest import mock

import pytest
from rasa.nlu import utils

from rasam import RegexEntityExtractor


@pytest.mark.parametrize(
    "meta, expected",
    ids=["empty", "has_regex"],
    argvalues=[
        ({}, []),
        (
            {"regex_features": [{"name": "STRING", "pattern": ".+"}]},
            [{"compiled": mock.ANY, "name": "STRING", "pattern": ".+"}],
        ),
    ],
)
@mock.patch.object(re, "compile")
def test_init(re_compile: mock.MagicMock, meta: Dict[str, Any], expected: List[Dict[str, Any]]) -> None:
    extractor = RegexEntityExtractor(meta)
    assert extractor.regex_features == expected
    if len(expected):
        re_compile.assert_called_once()
    else:
        re_compile.assert_not_called()


def test_train() -> None:
    training_data = mock.MagicMock()
    training_data.regex_features = []
    extractor = RegexEntityExtractor({})
    extractor.train(training_data)
    assert extractor.regex_features == training_data.regex_features


@pytest.mark.parametrize(
    "meta, expected",
    ids=["no_regex", "has_regex"],
    argvalues=[
        ({}, []),
        (
            {"regex_features": [{"name": "STRING", "pattern": "test"}]},
            [
                {
                    "start": 7,
                    "end": 11,
                    "value": "test",
                    "entity": "STRING",
                    "extractor": "RegexEntityExtractor",
                    "confidence": 1.0,
                }
            ],
        ),
    ],
)
def test_process(meta: Dict[str, Any], expected) -> None:
    training_data = mock.MagicMock()
    message = mock.MagicMock()
    message.text = 'input "test"'
    message.get.return_value = []
    training_data.regex_features = []
    extractor = RegexEntityExtractor(meta)
    extractor.process(message)
    message.set.assert_called_once_with("entities", expected, add_to_output=True)


@pytest.mark.parametrize(
    "regex_features, expected, persisted",
    ids=["no_regex_features", "with_regex_features"],
    argvalues=[
        ({}, {"file": None}, False),
        ([{"name": "STRING", "pattern": "test"}], {"file": "filename.json"}, True,),
    ],
)
@mock.patch.object(utils, "write_json_to_file")
def test_persist(
    write_json_to_file: mock.MagicMock, regex_features: Dict[str, Any], expected: Dict[str, Any], persisted: bool,
) -> None:
    training_data = mock.MagicMock()
    training_data.regex_features = regex_features
    extractor = RegexEntityExtractor({})
    extractor.train(training_data)
    assert expected == extractor.persist("filename", "model_dir")
    if persisted:
        write_json_to_file.assert_called_once_with(os.path.join("model_dir", "filename.json"), regex_features)
    else:
        write_json_to_file.assert_not_called()


@pytest.mark.parametrize("meta, loaded", [({"file": None}, False), ({"file": "test.json"}, True)])
@mock.patch.object(utils, "read_json_file")
def test_load(read_json_file: mock.MagicMock, meta: Dict[str, Any], loaded: bool) -> None:
    extractor = RegexEntityExtractor.load(meta, "model_dir")
    if loaded:
        read_json_file.assert_called_once_with(os.path.join("model_dir", "test.json"))
        assert isinstance(extractor, RegexEntityExtractor)
    else:
        read_json_file.assert_not_called()
