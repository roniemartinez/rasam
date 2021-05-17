import os
import re
from typing import Any, Dict, Optional, Set, Text

from rasa.nlu import utils
from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.model import Metadata
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.utils import io


class RegexEntityExtractor(EntityExtractor):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        self.regex_features = []
        if component_config is None:
            return
        for regex_feature in component_config.get("regex_features", []):
            regex_feature["compiled"] = re.compile(regex_feature["pattern"])
            self.regex_features.append(regex_feature)

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        self.regex_features = training_data.regex_features

    def process(self, message: Message, **kwargs: Any) -> None:
        matches: Set[Any] = set()
        for regex_feature in self.regex_features:
            for match in regex_feature["compiled"].finditer(message.data.get("text")):
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
        entities = message.get("entities", []) + list(map(dict, matches))

        message.set(
            "entities",
            sorted(entities, key=lambda x: x.get("confidence", 0), reverse=True),
            add_to_output=True,
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
        model_dir: Text,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ) -> "Component":
        file_name = meta.get("file")
        regex_features = []
        if file_name:
            regex_features = io.read_json_file(os.path.join(model_dir, file_name))
        meta["regex_features"] = regex_features
        return cls(meta)
