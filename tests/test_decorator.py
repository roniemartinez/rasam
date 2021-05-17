from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import rasam


@rasam.action
def action_hello_world(
    self: Action, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
) -> List[Dict[Text, Any]]:
    dispatcher.utter_message(text="Hello World!")
    return []


def test_action() -> None:
    assert issubclass(action_hello_world, Action)
    a = action_hello_world()
    assert a.name() == "action_hello_world"
