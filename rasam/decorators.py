#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from typing import Callable, Text, Type

from rasa_sdk import Action


def action(f: Callable) -> Type[Action]:
    class RasamAction(Action):
        def name(self) -> Text:
            return f.__name__

    setattr(RasamAction, "run", f)
    return RasamAction
