from typing import Callable, Text, Type

from rasa_sdk import Action


def action(f: Callable) -> Type[Action]:
    class RasamAction(Action):
        def name(self) -> Text:
            return f.__name__

    setattr(RasamAction, "run", f)
    return RasamAction
