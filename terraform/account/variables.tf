locals {
  account = contains(keys(var.accounts), terraform.workspace) ? var.accounts[terraform.workspace] : var.accounts.development
  default_tags = {
    application            = "Data-lpa"
    business-unit          = "OPG"
    environment-name       = terraform.workspace
    infrastructure-support = "OPG WebOps: opgteam@digital.justice.gov.uk"
    is-production          = terraform.workspace == "production" ? "true" : "false"
    owner                  = "OPG POAS"
    service-area           = "POAS"
    source-code            = "https://github.com/ministryofjustice/opg-data-lpa"
  }
}

variable "accounts" {
  type = map(
    object({
      account_id      = string
      account_name    = string
      opg_hosted_zone = string
      }
    )
  )
}

variable "default_role" {
  type = string
}

variable "management_role" {
  type = string
}
