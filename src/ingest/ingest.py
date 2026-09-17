"""
obs-workshop-ingest

Receives POST /orders and POST /workflow from API Gateway.
- /orders   : validates the payload and enqueues it to SQS.
- /workflow : emits an event to EventBridge (used by the audit rule) and
              returns 202.
"""
import json
import os
import uuid
import logging
# === TASK 4 SNIPPET 1 STARTS - ADD CODE BETWEEN THE COMMENTS ===

# === TASK 4 SNIPPET 1 ENDS ===

import boto3

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

sqs = boto3.client("sqs")
events = boto3.client("events")

QUEUE_URL = os.environ["QUEUE_URL"]
EVENT_BUS_NAME = os.environ["EVENT_BUS_NAME"]

def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }

# === TASK 4 SNIPPET 2 STARTS - ADD CODE BETWEEN THE COMMENTS ===

# === TASK 4 SNIPPET 2 ENDS ===

def handler(event, context):
    logger.info("Received request: %s", event.get("path"))

    path = event.get("path", "")
    try:
        payload = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        logger.error("Invalid JSON body")
        return _response(400, {"message": "Invalid JSON body"})

    if path.endswith("/workflow"):
        order_id = payload.get("orderId") or str(uuid.uuid4())
        events.put_events(
            Entries=[
                {
                    "Source": "obs.workshop.orders",
                    "DetailType": "OrderWorkflowRequested",
                    "Detail": json.dumps({"orderId": order_id, **payload}),
                    "EventBusName": EVENT_BUS_NAME,
                }
            ]
        )
        logger.info("Emitted workflow event for order %s", order_id)
        return _response(202, {"orderId": order_id, "status": "workflow-requested"})

    # Default: /orders — validate + enqueue
    if not payload.get("item"):
        return _response(400, {"message": "Field 'item' is required"})

    order_id = payload.get("orderId") or str(uuid.uuid4())
    message = {"orderId": order_id, **payload}
    sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps(message))
    # === TASK 4 SNIPPET 3 STARTS - ADD CODE BETWEEN THE COMMENTS ===

    # === TASK 4 SNIPPET 2 ENDS ===
    logger.info("Enqueued order %s", order_id)
    return _response(202, {"orderId": order_id, "status": "queued"})
