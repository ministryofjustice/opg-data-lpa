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
      elasticache_count   = number
      request_caching_ttl = number
    })
  )
}

variable "default_role" {
  type = string
}

variable "environment_mapping" {
  type = map(string)
}

variable "lambda_image_uri" {
  default     = null
  description = "The URI of the container image that contains your Lambda function. Optional if package_type is not Image."
  type        = string
}

variable "management_role" {
  type = string
}
