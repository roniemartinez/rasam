import logging
import re
from typing import Any, AsyncIterator, List, Optional, Text, Tuple

import faker
from faker import Faker
from rasa.shared.importers.rasa import RasaFileImporter
from rasa.shared.nlu.training_data import loading
from rasa.shared.nlu.training_data.entities_parser import find_entities_in_training_example
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

logger = logging.getLogger(__name__)


class PlaceholderImporter(RasaFileImporter):
    """
    PlaceholderImporter replaces placeholders with fake data. It enables you to write training data without worrying
    about other data like numbers, names, texts, etc.

    Usage in config.yml:

    ```yml
    importers:
        - name: rasam.PlaceholderImporter
          fake_data_count: 50
    ```

    If `fake_data_count` is not specified, the default value is 1.
    """

    DEFAULT_FAKE_DATA_COUNT = 1
    FAKE_MAP = {
        "integer": lambda faker_: faker_.pyint(min_value=-9999, max_value=9999),
        "decimal": lambda faker_: faker_.pyfloat(min_value=-9999, max_value=9999),
        "number": lambda faker_: getattr(faker_, faker_.random_choices(["pyint", "pyfloat"], length=1)[0])(
            min_value=-9999, max_value=9999
        ),
        "name": lambda faker_: faker_.name(),
        "first_name": lambda faker_: faker_.first_name(),
        "last_name": lambda faker_: faker_.last_name(),
        "text": lambda faker_: faker_.text(),
        "word": lambda faker_: faker_.word(),
        "paragraph": lambda faker_: faker_.paragraph(),
        "uri": lambda faker_: faker_.uri(),
        "url": lambda faker_: faker_.url(),
        "local_uri": lambda faker_: faker_.file_path(depth=faker_.random_int(min=1, max=5), extension="html"),
        "email": lambda faker_: faker_.email(),
        "date": lambda faker_: faker_.date(),
        "time": lambda faker_: faker_.time(),
        "month": lambda faker_: faker_.month_name(),
        "day": lambda faker_: faker_.day_of_week(),
        "timezone": lambda faker_: faker_.timezone(),
        "company": lambda faker_: faker_.company(),
        "license_plate": lambda faker_: faker_.license_plate(),
        "address": lambda faker_: faker_.address(),
        "city": lambda faker_: faker_.city(),
        "country": lambda faker_: faker_.country(),
        "user_agent": lambda faker_: faker_.user_agent(),
        "password": lambda faker_: faker_.password(),
        "user_name": lambda faker_: faker_.user_name(),
        "file_path": lambda faker_: faker_.file_path(),
    }

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        keys = "|".join(self.FAKE_MAP.keys())
        regex = f"(\\{{({keys}|any)\\}}|@({keys}|any)(?=([^\\w]|$|@)))"
        self.placeholder_regex = re.compile(regex)

    async def get_nlu_data(self, language: Optional[Text] = "en") -> TrainingData:
        fake_data_count = self.DEFAULT_FAKE_DATA_COUNT

        for importer in self.config["importers"]:
            if importer.get("name") == "rasam.PlaceholderImporter":
                fake_data_count = importer.get("fake_data_count", self.DEFAULT_FAKE_DATA_COUNT)

        faker_ = faker.Faker()
        faker_.seed_instance(fake_data_count)

        training_data = [loading.load_data(nlu_file, language) for nlu_file in self._nlu_files]

        new_training_data = []

        for data in training_data:
            training_examples = []
            example: Message
            for example in data.training_examples:
                if example.get("intent"):
                    matches = [i async for i in self.find_placeholders(example.data.get("text"))]
                    if matches:
                        async for new_message in self.replace_placeholders(example, faker_, matches, fake_data_count):
                            training_examples.append(new_message)
                    else:
                        training_examples.append(example)
                else:
                    training_examples.append(example)
            new_training_data.append(
                TrainingData(
                    training_examples, data.entity_synonyms, data.regex_features, data.lookup_tables, data.responses
                )
            )

        merged_training_data = TrainingData().merge(*new_training_data)
        merged_training_data._fill_response_phrases()
        return merged_training_data

    async def replace_placeholders(
        self, example: Message, faker_: Faker, matches: List[Tuple[Any, ...]], count: int
    ) -> AsyncIterator[Message]:
        original_text = await self.rebuild_original_text(example)
        for _ in range(count):
            text = await self.replace_placeholders_in_text(example.data.get("text"), faker_, matches)
            original_text = await self.replace_placeholders_in_text(original_text, faker_, matches)
            entities = find_entities_in_training_example(original_text)
            new_message = Message.build(text, example.get("intent"), entities)
            yield new_message

    async def replace_placeholders_in_text(self, text: str, faker_: Faker, matches: List[Tuple[Any, ...]]) -> str:
        """
        Replaces each placeholder in text from items in matches using the fake data.
        """
        for placeholder, faker_string, start in sorted(matches, key=lambda x: x[2], reverse=True):
            if faker_string == "any":
                faker_string = faker_.random_choices(list(self.FAKE_MAP.keys()), length=1)[0]
            text = text[:start] + text[start:].replace(placeholder, str(self.FAKE_MAP[faker_string](faker_)), 1)
        return text

    async def find_placeholders(self, text: str) -> AsyncIterator[Tuple[Any, ...]]:
        """
        Find placeholder names in text. See FAKE_MAP for valid placeholder names.

        Examples:
            hello {any}
            {name} went to {city}
            see you on @day at @time

        yields: Tuple(placeholder text, placeholder name, match start)
        """
        for item in self.placeholder_regex.finditer(text):
            yield *[i for i in item.groups() if i][:2], item.start()

    @staticmethod
    async def rebuild_original_text(example: Message) -> str:
        """
        Rebuilds original training text in Markdown form.
        """
        original_entities = example.get("entities")
        original_text = example.data.get("text")
        if original_entities:
            original_text = list(original_text)
            for entity in sorted(original_entities, key=lambda x: x.get("start"), reverse=True):
                start = entity["start"]
                end = entity["end"]
                value = entity["value"]
                name = entity["entity"]
                original_text[start:end] = f"[{value}]({name})"
            original_text = "".join(original_text)
        return original_text
