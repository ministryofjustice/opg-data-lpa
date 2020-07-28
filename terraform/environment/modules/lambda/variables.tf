variable "environment" {
  type = string
}

variable "aws_subnet_ids" {
  type = list(string)
}

variable "lambda_prefix" {
  type = string
}

variable "handler" {
  type = string
}

variable "lambda_function_subdir" {
  type = string
}

variable "tags" {}

variable "openapi_version" {}

variable "rest_api" {}

variable "account" {}
