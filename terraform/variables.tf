variable "aws_region" { type = string; default = "us-east-1" }
variable "environment" { type = string }
variable "container_image" { type = string; default = "placeholder" }

variable "stripe_secret_key_name" {
  type        = string
  description = "The name of the SSM parameter for the Stripe secret key."
  default     = "ssp/payment/stripe_secret_key"
}

variable "stripe_webhook_secret_name" {
  type        = string
  description = "The name of the SSM parameter for the Stripe webhook secret."
  default     = "ssp/payment/stripe_webhook_secret"
}
