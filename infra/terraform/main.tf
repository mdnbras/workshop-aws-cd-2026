data "aws_caller_identity" "current" {}

locals {
  topic_name              = "${var.name_prefix}-orders-topic"
  notification_queue_name = "${var.name_prefix}-notification-queue"
  analytics_queue_name    = "${var.name_prefix}-analytics-queue"
  notification_dlq_name   = "${var.name_prefix}-notification-dlq"
}

resource "aws_sns_topic" "orders" {
  name = local.topic_name
}

resource "aws_sqs_queue" "notification_dlq" {
  name                      = local.notification_dlq_name
  message_retention_seconds = 1209600
}

resource "aws_sqs_queue" "notification" {
  name                       = local.notification_queue_name
  visibility_timeout_seconds = var.visibility_timeout_seconds

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.notification_dlq.arn
    maxReceiveCount     = var.max_receive_count
  })
}

resource "aws_sqs_queue_redrive_allow_policy" "notification_dlq" {
  queue_url = aws_sqs_queue.notification_dlq.id

  redrive_allow_policy = jsonencode({
    redrivePermission = "byQueue"
    sourceQueueArns   = [aws_sqs_queue.notification.arn]
  })
}

resource "aws_sqs_queue" "analytics" {
  name                       = local.analytics_queue_name
  visibility_timeout_seconds = var.visibility_timeout_seconds
}

data "aws_iam_policy_document" "notification_queue" {
  statement {
    sid     = "AllowSnsPublish"
    effect  = "Allow"
    actions = ["sqs:SendMessage"]

    principals {
      type        = "Service"
      identifiers = ["sns.amazonaws.com"]
    }

    resources = [aws_sqs_queue.notification.arn]

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_sns_topic.orders.arn]
    }
  }
}

data "aws_iam_policy_document" "analytics_queue" {
  statement {
    sid     = "AllowSnsPublish"
    effect  = "Allow"
    actions = ["sqs:SendMessage"]

    principals {
      type        = "Service"
      identifiers = ["sns.amazonaws.com"]
    }

    resources = [aws_sqs_queue.analytics.arn]

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_sns_topic.orders.arn]
    }
  }
}

resource "aws_sqs_queue_policy" "notification" {
  queue_url = aws_sqs_queue.notification.id
  policy    = data.aws_iam_policy_document.notification_queue.json
}

resource "aws_sqs_queue_policy" "analytics" {
  queue_url = aws_sqs_queue.analytics.id
  policy    = data.aws_iam_policy_document.analytics_queue.json
}

resource "aws_sns_topic_subscription" "notification" {
  topic_arn            = aws_sns_topic.orders.arn
  protocol             = "sqs"
  endpoint             = aws_sqs_queue.notification.arn
  raw_message_delivery = true

  depends_on = [aws_sqs_queue_policy.notification]
}

resource "aws_sns_topic_subscription" "analytics" {
  topic_arn            = aws_sns_topic.orders.arn
  protocol             = "sqs"
  endpoint             = aws_sqs_queue.analytics.arn
  raw_message_delivery = true

  depends_on = [aws_sqs_queue_policy.analytics]
}
