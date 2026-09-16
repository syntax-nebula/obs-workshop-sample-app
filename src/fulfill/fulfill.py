"""
obs-workshop-fulfill  (Step Functions task)

Final workflow step: writes the validated order to DynamoDB with status 'fulfilled'.
Instrumented with Powertools:
  - Tracer auto-patches boto3 so the DynamoDB call shows as a subsegment
    (and DynamoDB appears as a downstream node on the X-Ray service map).
  - Logger emits structured JSON logs.
"""
import os

import boto3
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


@tracer.capture_lambda_handler
@logger.inject_lambda_context
def handler(event, context):
    order_id = event.get("orderId", "unknown")
    logger.append_keys(order_id=order_id)
    table.put_item(
        Item={
            "orderId": order_id,
            "item": event.get("item"),
            "quantity": event.get("quantity", 1),
            "status": "fulfilled",
        }
    )
    logger.info("Fulfilled order")
    return {**event, "fulfilled": True}
