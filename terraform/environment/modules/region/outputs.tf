output "lambda" {
  description = "Data LPA Lambda Object"
  value       = aws_lambda_function.data_lpa
}

output "lambda_security_group" {
  description = "Lambda Security Group Object"
  value       = aws_security_group.lambda
}
