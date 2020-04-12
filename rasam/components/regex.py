#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import os
import re
from typing import Any, Dict, Optional, Text

from rasa.nlu import utils
from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message, TrainingData


class RegexEntityExtractor(EntityExtractor):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        self.regex_features = []
        for regex_feature in component_config.get("regex_features", []):  # type: ignore
            regex_feature["compiled"] = re.compile(regex_feature["pattern"])
            self.regex_features.append(regex_feature)

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,) -> None:
        self.regex_features = training_data.regex_features

    def process(self, message: Message, **kwargs: Any) -> None:
        matches = set()
        for regex_feature in self.regex_features:
            for match in regex_feature["compiled"].finditer(message.text):
                matches.add(
                    tuple(
                        {
                            "start": match.start(),
                            "end": match.end(),
                            "value": match.group(0),
                            "entity": regex_feature["name"],
                            "extractor": self.name,
                            "confidence": 1.0,
                        }.items()
                    )
                )
        entities = message.get("entities", []) + list(map(dict, matches))  # type: ignore

        message.set(
            "entities", sorted(entities, key=lambda x: x.get("confidence", 0), reverse=True), add_to_output=True,
        )

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        if self.regex_features:
            file_name = file_name + ".json"
            utils.write_json_to_file(os.path.join(model_dir, file_name), self.regex_features)
            return {"file": file_name}
        return {"file": None}

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional[Metadata] = None,
        cached_component: Optional[Component] = None,
        **kwargs: Any,
    ) -> "EntityExtractor":
        file_name = meta.get("file")
        regex_features = []
        if file_name:
            regex_features = utils.read_json_file(os.path.join(model_dir, file_name))  # type: ignore
        meta["regex_features"] = regex_features
        return cls(meta)
