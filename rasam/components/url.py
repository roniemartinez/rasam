from typing import Any, Dict, Optional, Set, Text

import urlextract
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.shared.nlu.training_data.message import Message


class URLEntityExtractor(EntityExtractor):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        self.extractor = urlextract.URLExtract()

    def process(self, message: Message, **kwargs: Any) -> None:
        urls: Set[Any] = set()
        last_pos = 0
        for url in self.extractor.gen_urls(message.data.get("text")):
            start = message.data.get("text").find(url, last_pos)
            end = start + len(url)
            last_pos = end
            urls.add(
                tuple(
                    {
                        "start": start,
                        "end": end,
                        "value": url,
                        "entity": "URL",
                        "extractor": self.name,
                        "confidence": 1.0,
                    }.items()
                )
            )
        entities = message.get("entities", []) + list(
            sorted(map(dict, urls), key=lambda x: x.get("start"))  # type: ignore
        )

        message.set(
            "entities",
            sorted(entities, key=lambda x: x.get("confidence", 0), reverse=True),
            add_to_output=True,
        )
