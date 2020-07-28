data "aws_security_group" "lambda_api_ingress" {
  filter {
    name   = "tag:Name"
    values = ["integration-lambda-api-access-${var.account.target_environment}"]
  }
}
