"""
obs-workshop-validate

Validates an order passed in by the state machine. Returns the order with a
validated flag.
"""
import logging
import os

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


def handler(event, context):
    logger.info("Validating order: %s", event.get("orderId"))
    item = event.get("item")
    if not item:
        # Make a failed state in the workflow.
        raise ValueError("Order is missing required field 'item'")
    return {**event, "validated": True}
