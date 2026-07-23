variable "accounts" {
  type = map(
    object({
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
    })
  )
}

variable "default_role" {
  type = string
}

variable "environment_mapping" {
  type = map(string)
}

variable "lambda_image_tag" {
  description = "The Tag of the Lambda Image to Deploy"
  type        = string
}

variable "management_role" {
  type = string
}
