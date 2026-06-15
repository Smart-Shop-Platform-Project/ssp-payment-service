output "ecr_repository_url" {
  value       = module.ecr.repository_url
  description = "The URL of the ECR repository."
}

output "lambda_function_name" {
  value       = module.lambda_service.function_name
  description = "The name of the Lambda function."
}
