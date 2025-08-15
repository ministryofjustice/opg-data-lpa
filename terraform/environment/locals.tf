locals {
  environment        = replace(terraform.workspace, "_", "-")
  account            = contains(keys(var.accounts), local.environment) ? var.accounts[local.environment] : var.accounts.development
  branch_build_flag  = contains(keys(var.accounts), local.environment) ? false : true
  a_record           = local.branch_build_flag ? lower("${local.environment}.${data.aws_route53_zone.environment_cert.name}") : lower(data.aws_route53_zone.environment_cert.name)
  redis_c_name       = local.branch_build_flag ? lower("${local.environment}-redis.${data.aws_route53_zone.environment_cert.name}") : lower("redis.${data.aws_route53_zone.environment_cert.name}")
  redis_c_rg_name    = substr(local.environment, 0, 26)
  target_environment = contains(keys(var.environment_mapping), local.environment) ? var.environment_mapping[local.environment] : var.environment_mapping.default

  default_tags = {
    business-unit          = "OPG"
    application            = "Data-lpa"
    environment-name       = local.environment
    owner                  = "OPG Supervision"
    infrastructure-support = "OPG WebOps: opgteam@digital.justice.gov.uk"
    is-production          = local.account.is_production
    source-code            = "https://github.com/ministryofjustice/opg-data-lpa"
  }

  api_name = "lpa"

  api_template_vars = {
    region            = "eu-west-1"
    environment       = local.environment
    allowed_roles     = join(", ", local.account.allowed_roles)
    allowed_ip_ranges = []
    account_id        = local.account.account_id
  }

  //Modify here for new version - replace with new code (comment out old code)
  latest_openapi_version = "v1"
  openapi_spec           = "../../lambda_functions/${local.latest_openapi_version}/openapi/${local.api_name}-openapi.yml"
}
