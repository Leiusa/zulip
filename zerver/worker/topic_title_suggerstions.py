# zerver/worker/topic_title_suggestions.py
from typing import Any
import logging

from zerver.worker.base import QueueProcessingWorker

logger = logging.getLogger(__name__)

class TopicTitleSuggestionsWorker(QueueProcessingWorker):
    queue_name = "topic_title_suggestions"

    def consume(self, event: dict[str, Any]) -> None:
        logger.info("Topic title suggestion event received: %s", event)