#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from typing import Any, Dict, Optional, Text

import urlextract
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.training_data import Message


class URLEntityExtractor(EntityExtractor):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        self.extractor = urlextract.URLExtract()

    def process(self, message: Message, **kwargs: Any) -> None:
        urls = set()
        last_pos = 0
        for url in self.extractor.gen_urls(message.text):
            start = message.text.find(url, last_pos)
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
            "entities", sorted(entities, key=lambda x: x.get("confidence", 0), reverse=True), add_to_output=True
        )
