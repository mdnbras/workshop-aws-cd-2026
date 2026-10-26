output "aws_account_id" {
  description = "AWS account where the workshop resources were created."
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "AWS region used by the workshop."
  value       = var.aws_region
}

output "orders_topic_arn" {
  description = "SNS topic ARN used by the Order API."
  value       = aws_sns_topic.orders.arn
}

output "notification_queue_url" {
  description = "SQS URL used by the notification worker."
  value       = aws_sqs_queue.notification.id
}

output "notification_queue_arn" {
  description = "Notification queue ARN."
  value       = aws_sqs_queue.notification.arn
}

output "analytics_queue_url" {
  description = "SQS URL used by the analytics worker."
  value       = aws_sqs_queue.analytics.id
}

output "analytics_queue_arn" {
  description = "Analytics queue ARN."
  value       = aws_sqs_queue.analytics.arn
}

output "notification_dlq_url" {
  description = "Dead Letter Queue URL."
  value       = aws_sqs_queue.notification_dlq.id
}

output "notification_dlq_arn" {
  description = "Dead Letter Queue ARN."
  value       = aws_sqs_queue.notification_dlq.arn
}
