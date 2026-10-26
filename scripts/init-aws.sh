#!/bin/sh
set -eu

ENDPOINT="${AWS_ENDPOINT_URL:-http://floci:4566}"
REGION="${AWS_DEFAULT_REGION:-us-east-1}"
ACCOUNT_ID="000000000000"
TOPIC_ARN="arn:aws:sns:${REGION}:${ACCOUNT_ID}:orders-topic"

aws_local() {
  aws --endpoint-url "$ENDPOINT" --region "$REGION" "$@"
}

echo "[aws-init] waiting for Floci at ${ENDPOINT}..."
until aws_local sts get-caller-identity >/dev/null 2>&1; do
  sleep 1
done

echo "[aws-init] creating SNS topic..."
aws_local sns create-topic --name orders-topic >/dev/null

echo "[aws-init] creating queues..."
aws_local sqs create-queue --queue-name notification-dlq >/dev/null
aws_local sqs create-queue --queue-name notification-queue --attributes VisibilityTimeout=5 >/dev/null
aws_local sqs create-queue --queue-name analytics-queue --attributes VisibilityTimeout=5 >/dev/null

NOTIFICATION_QUEUE_URL="${ENDPOINT}/${ACCOUNT_ID}/notification-queue"
ANALYTICS_QUEUE_URL="${ENDPOINT}/${ACCOUNT_ID}/analytics-queue"
DLQ_URL="${ENDPOINT}/${ACCOUNT_ID}/notification-dlq"

DLQ_ARN=$(aws_local sqs get-queue-attributes \
  --queue-url "$DLQ_URL" \
  --attribute-names QueueArn \
  --query 'Attributes.QueueArn' \
  --output text)

NOTIFICATION_QUEUE_ARN=$(aws_local sqs get-queue-attributes \
  --queue-url "$NOTIFICATION_QUEUE_URL" \
  --attribute-names QueueArn \
  --query 'Attributes.QueueArn' \
  --output text)

ANALYTICS_QUEUE_ARN=$(aws_local sqs get-queue-attributes \
  --queue-url "$ANALYTICS_QUEUE_URL" \
  --attribute-names QueueArn \
  --query 'Attributes.QueueArn' \
  --output text)

REDRIVE_POLICY="{\"deadLetterTargetArn\":\"${DLQ_ARN}\",\"maxReceiveCount\":\"3\"}"
aws_local sqs set-queue-attributes \
  --queue-url "$NOTIFICATION_QUEUE_URL" \
  --attributes "RedrivePolicy=${REDRIVE_POLICY}"

# Recriar o laboratório deve ser seguro. Removemos subscriptions antigas antes de assinar novamente.
for SUB_ARN in $(aws_local sns list-subscriptions-by-topic \
  --topic-arn "$TOPIC_ARN" \
  --query 'Subscriptions[].SubscriptionArn' \
  --output text 2>/dev/null || true); do
  [ "$SUB_ARN" = "None" ] || aws_local sns unsubscribe --subscription-arn "$SUB_ARN" >/dev/null 2>&1 || true
done

aws_local sns subscribe \
  --topic-arn "$TOPIC_ARN" \
  --protocol sqs \
  --notification-endpoint "$NOTIFICATION_QUEUE_ARN" \
  --attributes RawMessageDelivery=true >/dev/null

aws_local sns subscribe \
  --topic-arn "$TOPIC_ARN" \
  --protocol sqs \
  --notification-endpoint "$ANALYTICS_QUEUE_ARN" \
  --attributes RawMessageDelivery=true >/dev/null

echo "[aws-init] local AWS ready"
echo "[aws-init] topic: ${TOPIC_ARN}"
echo "[aws-init] queue: ${NOTIFICATION_QUEUE_URL}"
echo "[aws-init] queue: ${ANALYTICS_QUEUE_URL}"
echo "[aws-init] dlq:   ${DLQ_URL}"
