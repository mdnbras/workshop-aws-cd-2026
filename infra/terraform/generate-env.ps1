$ErrorActionPreference = "Stop"

$RootDir = Resolve-Path (Join-Path $PSScriptRoot "../..")
$OutFile = Join-Path $RootDir ".env.aws"

$AwsRegion = terraform output -raw aws_region
$OrdersTopicArn = terraform output -raw orders_topic_arn
$NotificationQueueUrl = terraform output -raw notification_queue_url
$AnalyticsQueueUrl = terraform output -raw analytics_queue_url

@"
AWS_REGION=$AwsRegion
ORDERS_TOPIC_ARN=$OrdersTopicArn
NOTIFICATION_QUEUE_URL=$NotificationQueueUrl
ANALYTICS_QUEUE_URL=$AnalyticsQueueUrl
"@ | Set-Content -Path $OutFile -Encoding UTF8

Write-Host "Generated $OutFile"
Write-Host "AWS credentials are intentionally not written to this file."
