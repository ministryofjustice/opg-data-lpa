variable "account" {
  type = object({
    account_id          = string
    account_mapping     = string
    active_regions      = map(bool)
    allowed_roles       = list(string)
    is_production       = string
    logger_level        = string
    opg_hosted_zone     = string
    vpc_id              = string
    session_data        = string
    elasticache_count   = number
    request_caching_ttl = number
    }
  )
}

variable "environment" {
  description = "Name of the Environment"
  type        = string
}

variable "lambda_iam_role" {
  description = "IAM Role Object of the Lambda Role"
  type = object({
    arn  = string
    name = string
  })
}

variable "lambda_image_tag" {
  description = "The Tag of the container image to deploy"
  type        = string
}

variable "region" {
  description = "Region in which to deploy the resources"
  type        = string
}

variable "target_environment" {
  description = "Sirius Environment the Lambda will connect to"
  type        = string
}

variable "tmp_execution_arn" {
  type = string
}

variable "tmp_redis_endpoint" {
  type = string
}

variable "tmp_redis_sg_id" {
  type = string
}
