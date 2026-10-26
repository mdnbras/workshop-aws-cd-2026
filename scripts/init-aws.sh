#!/bin/sh
set -eu

ENDPOINT="${AWS_ENDPOINT_URL:-http://floci:4566}"
REGION="${AWS_DEFAULT_REGION:-us-east-1}"

aws_local() {
  aws --endpoint-url "$ENDPOINT" --region "$REGION" "$@"
}

echo "[aws-init] waiting for Floci..."
until aws_local sns list-topics >/dev/null 2>&1; do sleep 1; done

echo "[aws-init] creating orders-topic..."
aws_local sns create-topic --name orders-topic >/dev/null

echo "[aws-init] producer step ready"
