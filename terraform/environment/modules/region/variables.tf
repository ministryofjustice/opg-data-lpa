variable "environment" {
  type = object({
    account_id                = string
    account_name              = string
    active_regions            = map(bool)
    allowed_roles             = list(string)
    is_production             = string
    logger_level              = string
    opg_hosted_zone           = string
    session_data              = string
    elasticache_node_count    = number
    elasticache_instance_type = string
    request_caching_ttl       = number
    }
  )
}

variable "environment_name" {
  description = "Name of the Environment"
  type        = string
}

variable "is_ephemeral" {
  description = "Whether this is an ephemeral environment"
  type        = bool
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

variable "region_active" {
  description = "Whether this region is active"
  type        = bool
}

variable "sirius_environment" {
  description = "Sirius Environment the Lambda will connect to"
  type        = string
}
