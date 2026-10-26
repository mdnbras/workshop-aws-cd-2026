#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_FILE="${ROOT_DIR}/.env.aws"

cat > "${OUT_FILE}" <<EOF
AWS_REGION=$(terraform output -raw aws_region)
ORDERS_TOPIC_ARN=$(terraform output -raw orders_topic_arn)
NOTIFICATION_QUEUE_URL=$(terraform output -raw notification_queue_url)
ANALYTICS_QUEUE_URL=$(terraform output -raw analytics_queue_url)
EOF

echo "Generated ${OUT_FILE}"
echo "AWS credentials are intentionally not written to this file."
