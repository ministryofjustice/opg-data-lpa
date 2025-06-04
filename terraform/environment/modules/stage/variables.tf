variable "account_name" {}

variable "api_name" {}

variable "aws_subnet_ids" {
  type = list(string)
}

variable "domain_name" {}

variable "environment" {
  type = string
}

variable "openapi_version" {}

variable "region_name" {}

variable "rest_api" {}

variable "tags" {}

variable "vpc_id" {
  type = string
}

variable "content_api_sha" {
  type = string
}

variable "content_api_policy_sha" {
  type = string
}

variable "lpa_lambda_function_name" {
  type        = string
  description = "The name of the Lambda function"
}

variable "lpa_lambda_source_code_hash" {
  type        = string
  description = "The source code hash of the Lambda function"
}
