#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from typing import Any, Dict, List, Tuple

import asynctest
import faker
import pytest
from rasa.nlu.training_data import Message, TrainingData, loading

from rasam import PlaceholderImporter


@asynctest.patch.object(loading, "load_data")
@asynctest.patch.object(faker, "Faker")
@pytest.mark.asyncio
async def test_get_nlu_data(Faker: asynctest.MagicMock, load_data: asynctest.MagicMock) -> None:
    faker_ = Faker()
    faker_.name.return_value = "Nikola Tesla"
    training_data = TrainingData(
        training_examples=[
            Message.build("hello", "intent_test"),
            Message.build("hello @name", "intent_test"),
            Message.build("hello"),
        ]
    )
    load_data.return_value = training_data

    importer = PlaceholderImporter()
    importer.config = {"importers": [{"name": "rasam.PlaceholderImporter"}]}
    importer._nlu_files = ["test"]
    new_training_data = await importer.get_nlu_data()

    faker_.seed_instance.assert_called_once_with(importer.DEFAULT_FAKE_DATA_COUNT)
    load_data.assert_called_once_with("test", "en")
    message: Message
    expected_messages = [
        Message.build("hello", "intent_test"),
        Message.build("hello Nikola Tesla", "intent_test"),
        Message.build("hello"),
    ]
    for message, expected in zip(new_training_data.training_examples, expected_messages):
        assert message.get("intent") == expected.get("intent")
        assert message.get("text") == expected.get("text")


@pytest.mark.parametrize(
    "test, text, fake_data, matches, count, expected",
    [
        (
            "simple test",
            "hello @name",
            ["Nikola Tesla", "Nikola Tesla"],
            [("@name", "name", 6)],
            1,
            ["hello Nikola Tesla"],
        ),
        (
            "2 fake data",
            "hello @name",
            ["Nikola Tesla", "Nikola Tesla", "Thomas Edison", "Thomas Edison"],
            [("@name", "name", 6)],
            2,
            ["hello Nikola Tesla", "hello Thomas Edison"],
        ),
    ],
)
@asynctest.patch.object(faker, "Faker")
@pytest.mark.asyncio
async def test_replace_placeholders(
    faker_: asynctest.MagicMock,
    test: str,
    text: str,
    fake_data: List[str],
    matches: List[Tuple[str, str, int]],
    count: int,
    expected: List[str],
) -> None:
    faker_.name.side_effect = fake_data
    importer = PlaceholderImporter()
    message = Message.build(text)
    index = 0
    async for new_message in importer.replace_placeholders(message, faker_, matches, count):
        print(new_message.as_dict())
        assert new_message.text == expected[index]
        index += 1
    assert index == count


@pytest.mark.parametrize(
    "test, text, fake_data, matches, expected",
    [
        (
            "single placeholder",
            "hello {name}",
            {"name": ["Nikola Tesla"]},
            [("{name}", "name", 6)],
            "hello Nikola Tesla",
        ),
        (
            "repeated {} placeholders",
            "hello {name} and {name}",
            {"name": ["Thomas Edison", "Nikola Tesla"]},
            [("{name}", "name", 6), ("{name}", "name", 16)],
            "hello Nikola Tesla and Thomas Edison",
        ),
        (
            "mixed repeated placeholders",
            "hello @name and {name}",
            {"name": ["Thomas Edison", "Nikola Tesla"]},
            [("@name", "name", 6), ("{name}", "name", 16)],
            "hello Nikola Tesla and Thomas Edison",
        ),
        (
            "multiple placeholders",
            "call me on @day at {time}",
            {"day_of_week": ["Monday"], "time": ["12:00"]},
            [("@day", "day", 11), ("{time}", "time", 19)],
            "call me on Monday at 12:00",
        ),
        (
            "single number",
            "{number}",
            {"random_choices": [["integer"]], "integer": ["123"]},
            [("{number}", "number", 0)],
            "123",
        ),
        (
            "multiple numbers",
            "add @number and @number",
            {"random_choices": [["integer"], ["integer"]], "integer": ["456", "123"]},
            [("@number", "number", 4), ("@number", "number", 16)],
            "add 123 and 456",
        ),
        (
            "single any",
            "{any}",
            {"random_choices": [["name"]], "name": ["Nikola Tesla"]},
            [("{any}", "any", 0)],
            "Nikola Tesla",
        ),
        (
            "multiple any",
            "I saw @any and @any",
            {"random_choices": [["name"], ["name"]], "name": ["Thomas Edison", "Nikola Tesla"]},
            [("@any", "any", 6), ("@any", "any", 15)],
            "I saw Nikola Tesla and Thomas Edison",
        ),
        (
            "@ placeholder followed by letters should not be replaced",
            "hello @names and @name",
            {"name": ["Thomas Edison"]},
            [("@name", "name", 17)],
            "hello @names and Thomas Edison",
        ),
    ],
)
@asynctest.patch.object(faker, "Faker")
@pytest.mark.asyncio
async def test_replace_placeholders_in_text(
    faker_: asynctest.MagicMock,
    test: str,
    text: str,
    fake_data: Dict[str, List[str]],
    matches: List[Tuple[str, str, int]],
    expected: str,
) -> None:
    for method, data in fake_data.items():
        getattr(faker_, method).side_effect = data
    importer = PlaceholderImporter()
    formatted_text = await importer.replace_placeholders_in_text(text, faker_, matches)
    assert formatted_text == expected, test


@pytest.mark.parametrize(
    "test, text, expected",
    [
        ("single curly braces", "hello {any}", [("{any}", "any", 6)]),
        ("multiple curly braces", "hello {any}, {any}", [("{any}", "any", 6), ("{any}", "any", 13)]),
        ("single @ placeholder", "hello @any", [("@any", "any", 6)]),
        ("multiple @ placeholder", "hello @any @any", [("@any", "any", 6), ("@any", "any", 11)]),
        ("mixed placeholders", "hello {any} @any", [("{any}", "any", 6), ("@any", "any", 12)]),
        ("unknown placeholders", "hello {testing} @testing", []),
        ("existing placeholder but appended with text", "hello @anyhow", []),
        ("@ placeholders without spaces", "hello @any@any", [("@any", "any", 6), ("@any", "any", 10)]),
        ("{} placeholder without spaces", "hello {any}how@any", [("{any}", "any", 6), ("@any", "any", 14)]),
    ],
)
@pytest.mark.asyncio
async def test_find_placeholders(test: str, text: str, expected: List[Tuple[str, str, int]]) -> None:
    importer = PlaceholderImporter()
    placeholders = [placeholder async for placeholder in importer.find_placeholders(text)]
    assert placeholders == expected, test


@pytest.mark.parametrize(
    "text, entities, expected",
    [
        ("hello world", [], "hello world"),
        ("hello world", [{"start": 0, "end": 5, "value": "hello", "entity": "GREETING"}], "[hello](GREETING) world"),
        (
            "hello world",
            [
                {"start": 0, "end": 5, "value": "hello", "entity": "GREETING"},
                {"start": 6, "end": 11, "value": "world", "entity": "LOCATION"},
            ],
            "[hello](GREETING) [world](LOCATION)",
        ),
    ],
)
@pytest.mark.asyncio
async def test_rebuild_original_text(text: str, entities: List[Dict[str, Any]], expected: str) -> None:
    message = Message.build(text, "test_intent", entities)
    original_text = await PlaceholderImporter.rebuild_original_text(message)
    assert expected == original_text
