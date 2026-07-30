locals {
  account            = contains(keys(var.accounts), local.environment) ? var.accounts[local.environment] : var.accounts.ephemeral
  environment        = replace(terraform.workspace, "_", "-")
  is_ephemeral       = contains(keys(var.accounts), local.environment) ? false : true
  target_environment = contains(keys(var.environment_mapping), local.environment) ? var.environment_mapping[local.environment] : var.environment_mapping.default

  default_tags = {
    application            = "Data-lpa"
    business-unit          = "OPG"
    environment-name       = local.environment
    infrastructure-support = "OPG WebOps: opgteam@digital.justice.gov.uk"
    is-production          = local.account.is_production
    owner                  = "OPG POAS"
    service-area           = "POAS"
    source-code            = "https://github.com/ministryofjustice/opg-data-lpa"
  }
}
