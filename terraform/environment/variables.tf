variable "default_role" {
  default = "integrations-ci"
}

variable "management_role" {
  default = "integrations-ci"
}

variable "accounts" {
  type = map(
    object({
      account_id         = string
      account_mapping    = string
      allowed_roles      = list(string)
      is_production      = string
      logger_level       = string
      opg_hosted_zone    = string
      vpc_id             = string
      session_data       = string
      target_environment = string
      threshold          = number
      elasticache_count  = number
    })
  )
}
