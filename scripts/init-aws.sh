#!/bin/sh
set -eu
ENDPOINT="${AWS_ENDPOINT_URL:-http://floci:4566}"
REGION="${AWS_DEFAULT_REGION:-us-east-1}"
ACCOUNT_ID="000000000000"
TOPIC_ARN="arn:aws:sns:${REGION}:${ACCOUNT_ID}:orders-topic"
aws_local(){ aws --endpoint-url "$ENDPOINT" --region "$REGION" "$@"; }
until aws_local sns list-topics >/dev/null 2>&1; do sleep 1; done
aws_local sns create-topic --name orders-topic >/dev/null
aws_local sqs create-queue --queue-name notification-queue >/dev/null
aws_local sqs create-queue --queue-name analytics-queue >/dev/null
N_URL="${ENDPOINT}/${ACCOUNT_ID}/notification-queue"
A_URL="${ENDPOINT}/${ACCOUNT_ID}/analytics-queue"
N_ARN=$(aws_local sqs get-queue-attributes --queue-url "$N_URL" --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)
A_ARN=$(aws_local sqs get-queue-attributes --queue-url "$A_URL" --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)
for SUB_ARN in $(aws_local sns list-subscriptions-by-topic --topic-arn "$TOPIC_ARN" --query 'Subscriptions[].SubscriptionArn' --output text 2>/dev/null || true); do [ "$SUB_ARN" = "None" ] || aws_local sns unsubscribe --subscription-arn "$SUB_ARN" >/dev/null 2>&1 || true; done
aws_local sns subscribe --topic-arn "$TOPIC_ARN" --protocol sqs --notification-endpoint "$N_ARN" --attributes RawMessageDelivery=true >/dev/null
aws_local sns subscribe --topic-arn "$TOPIC_ARN" --protocol sqs --notification-endpoint "$A_ARN" --attributes RawMessageDelivery=true >/dev/null
echo "[aws-init] fan-out ready"
