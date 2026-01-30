from typing import Any

from zerver.lib.queue import get_queue_client

def enqueue_topic_title_suggestion_event(event: dict[str, object]) -> None:
    get_queue_client().json_publish("topic_title_suggestions", event)