terraform {
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
  backend "s3" {}
}

provider "aws" { region = var.aws_region }

data "aws_caller_identity" "current" {}

# IAM Policy for SSM Parameter Store Access
resource "aws_iam_policy" "ssm_policy" {
  name        = "ssp-payment-service-ssm-policy-${var.environment}"
  description = "Allows reading specific SSM parameters for the payment service"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "ssm:GetParameter",
        Effect   = "Allow",
        Resource = [
          "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/${var.stripe_secret_key_name}",
          "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/${var.stripe_webhook_secret_name}"
        ]
      }
    ]
  })
}

module "ecr" {
  source          = "git::https://github.com/DeathGod049/terraform-infra-child.git//modules/ecr?ref=v0.1.0"
  repository_name = "ssp-payment-service"
  environment     = var.environment
}

module "lambda_service" {
  source              = "git::https://github.com/DeathGod049/terraform-infra-child.git//modules/lambda-service?ref=v0.1.0"
  function_name       = "ssp-payment-service"
  environment         = var.environment
  container_image     = var.container_image

  execution_policy_arns = [aws_iam_policy.ssm_policy.arn]

  environment_variables = {
    STRIPE_SECRET_KEY_NAME     = var.stripe_secret_key_name
    STRIPE_WEBHOOK_SECRET_NAME = var.stripe_webhook_secret_name
    AWS_REGION                 = var.aws_region
  }
}
