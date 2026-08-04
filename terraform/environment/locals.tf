locals {
  environment        = contains(keys(var.environment), local.environment_name) ? var.environment[local.environment_name] : var.environment.ephemeral
  environment_name   = replace(terraform.workspace, "_", "-")
  is_ephemeral       = contains(keys(var.environment), local.environment_name) ? false : true
  sirius_environment = contains(keys(var.environment_mapping), local.environment_name) ? var.environment_mapping[local.environment_name] : var.environment_mapping.default

  default_tags = {
    application            = "Data-lpa"
    business-unit          = "OPG"
    environment-name       = local.environment_name
    infrastructure-support = "OPG WebOps: opgteam@digital.justice.gov.uk"
    is-production          = local.environment.is_production
    owner                  = "OPG POAS"
    service-area           = "POAS"
    source-code            = "https://github.com/ministryofjustice/opg-data-lpa"
  }
}
