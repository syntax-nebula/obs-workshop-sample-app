"""
obs-workshop-audit  (EventBridge rule target)

Invoked by the EventBridge rule on the custom bus for 'obs.workshop.orders' events.
"""
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


def handler(event, context):
    # === UNCOMMENT FOR TRIGGERING A FAILURE ===
    # logger.error("Audit deliberately failing to demo on-failure destination")
    # raise RuntimeError("Simulated audit failure")

    # === COMMENT OUT THESE TWO LINES IF YOU UNCOMMENT THE ONES ABOVE
    logger.info("Audit event received: %s", json.dumps(event.get("detail", {})))
    return {"audited": True}
