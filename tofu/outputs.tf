output "url" {
  description = "The URL of the website"
  value       = "https://${local.domain}"
}

output "distribution_id" {
  description = "The ID of the distribution, for aws cloudfront create-invalidation"
  value       = aws_cloudfront_distribution.site.id
}

output "function_name" {
  description = "The name of the function, for aws lambda update-function-code"
  value       = aws_lambda_function.site.function_name
}

output "log_group" {
  description = "The log group of the function, for aws logs tail"
  value       = aws_cloudwatch_log_group.function.name
}

output "deploy_role" {
  description = "The role of the deployment of the environment production, for role-to-assume of the workflow Build"
  value       = aws_iam_role.deploy.arn
}
