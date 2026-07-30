variable "account" {
  type = object({
    account_id      = string
    account_name    = string
    opg_hosted_zone = string
    }
  )
}

variable "region" {
  description = "Region to deploy resources into"
  type        = string
}
