locals {
  environment       = substr(replace(terraform.workspace, "_", "-"), 0, 40)
  account           = contains(keys(var.accounts), local.environment) ? var.accounts[local.environment] : var.accounts.development
  branch_build_flag = contains(keys(var.accounts), local.environment) ? false : true
  a_record          = local.branch_build_flag ? "${local.environment}.${data.aws_route53_zone.environment_cert.name}" : data.aws_route53_zone.environment_cert.name
  redis_c_name      = local.branch_build_flag ? "${local.environment}-redis.${data.aws_route53_zone.environment_cert.name}" : "redis.${data.aws_route53_zone.environment_cert.name}"

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
    region        = "eu-west-1"
    environment   = local.environment
    allowed_roles = join(", ", local.account.allowed_roles)
    account_id    = local.account.account_id
  }

  //Modify here for new version - replace with new code (comment out old code)
  latest_openapi_version = "v1"
  openapispec            = file("../../lambda_functions/${local.latest_openapi_version}/openapi/${local.api_name}-openapi.yml")
}

output "policy" {
  value = aws_api_gateway_rest_api.lpa.policy
}

output "rest_arn" {
  value = aws_api_gateway_rest_api.lpa.execution_arn
}

