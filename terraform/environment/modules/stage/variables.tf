variable "account_name" {
  type = string
}

variable "content_api_policy_sha" {
  type = string
}

variable "content_api_sha" {
  type = string
}

variable "domain_name" {
  type = object({})
}

variable "lpa_lambda_function_name" {
  type        = string
  description = "The name of the Lambda function"
}

variable "lpa_lambda_source_code_hash" {
  type        = string
  description = "The source code hash of the Lambda function"
}

variable "openapi_version" {
  type = string
}

variable "region_name" {
  type = string
}

variable "rest_api" {
  type = object({
    id   = string
    name = string
  })
}

variable "tags" {
  type = any
}
