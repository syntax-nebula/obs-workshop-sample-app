"""
obs-workshop-process

Triggered by the SQS OrdersQueue. Writes each order to DynamoDB.
Fails intermittently (FAIL_RATE, default 0.2).
"""
import json
import os
import random
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

FAIL_RATE = float(os.environ.get("FAIL_RATE", "0.2"))


def handler(event, context):
    for record in event.get("Records", []):
        body = json.loads(record["body"])
        order_id = body.get("orderId", "unknown")

        # Intentional, controllable failure path.
        if random.random() < FAIL_RATE:
            logger.error("Processing failed for order %s", order_id)
            raise RuntimeError(f"Intermittent processing error for order {order_id}")

        table.put_item(
            Item={
                "orderId": order_id,
                "item": body.get("item"),
                "quantity": body.get("quantity", 1),
                "status": "processed",
            }
        )
        logger.info("Processed order %s", order_id)

    return {"processed": len(event.get("Records", []))}
