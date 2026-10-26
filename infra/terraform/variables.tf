variable "aws_region" {
  description = "AWS region used by the workshop resources."
  type        = string
  default     = "us-east-1"
}

variable "name_prefix" {
  description = "Prefix used to identify workshop resources."
  type        = string
  default     = "workshop-eda"
}

variable "visibility_timeout_seconds" {
  description = "Visibility timeout used by the workshop queues."
  type        = number
  default     = 15
}

variable "max_receive_count" {
  description = "Number of receives before the notification message is sent to the DLQ."
  type        = number
  default     = 3
}

variable "tags" {
  description = "Additional tags applied to workshop resources."
  type        = map(string)
  default = {
    Project   = "workshop-aws-cd-2026"
    ManagedBy = "Terraform"
    Purpose   = "AWS Workshop"
  }
}
