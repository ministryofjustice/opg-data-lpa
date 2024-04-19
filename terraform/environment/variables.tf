variable "default_role" {
  default = "integrations-ci"
}

variable "management_role" {
  default = "integrations-ci"
}

variable "accounts" {
  type = map(
    object({
      account_id          = string
      account_mapping     = string
      allowed_roles       = list(string)
      is_production       = string
      logger_level        = string
      opg_hosted_zone     = string
      vpc_id              = string
      session_data        = string
      target_environment  = string
      elasticache_count   = number
      request_caching_ttl = number
    })
  )
}

variable "lambda_image_uri" {
  type        = string
  description = "The URI of the container image that contains your Lambda function. Optional if package_type is not Image."
  default     = null
}