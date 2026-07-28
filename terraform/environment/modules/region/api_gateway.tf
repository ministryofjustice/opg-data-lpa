locals {
  allow_list_mapping = {
    development = concat(
      module.allow_list.make_an_lpa_development,
      module.allow_list.make_an_lpa_preproduction,
      module.allow_list.use_an_lpa_development,
      module.allow_list.use_an_lpa_preproduction,
      module.allow_list.sirius_dev_allow_list,
    )
    preproduction = concat(
      module.allow_list.make_an_lpa_preproduction,
      module.allow_list.use_an_lpa_preproduction,
      module.allow_list.sirius_pre_allow_list,
    )
    production = concat(
      module.allow_list.make_an_lpa_production,
      module.allow_list.use_an_lpa_production,
      module.allow_list.sirius_prod_allow_list,
    )
  }

  api_gateway_policy_sha  = substr(base64sha256(data.aws_iam_policy_document.lpa_rest_api_policy.json), 0, 5)
  ip_restrictions_enabled = contains(["preproduction", "production"], var.account.account_mapping)
  open_api_spec = templatefile(
    "${path.module}/../../../../lambda_functions/v1/openapi/lpa-openapi.yml",
    {
      region      = var.region
      environment = var.environment
      account_id  = var.account.account_id
    }
  )
  open_api_spec_sha = substr(replace(base64sha256(local.open_api_spec), "/[^0-9A-Za-z_]/", ""), 0, 5)
}

resource "aws_api_gateway_rest_api" "lpa" {
  name        = "lpa-${var.environment}"
  description = "API Gateway for LPA - ${var.environment}"
  body        = local.open_api_spec
  policy      = sensitive(data.aws_iam_policy_document.lpa_rest_api_policy.json)

  endpoint_configuration {
    types = ["REGIONAL"]
  }
  region = var.region
}

data "aws_iam_policy_document" "lpa_rest_api_policy" {
  override_policy_documents = local.ip_restrictions_enabled ? [data.aws_iam_policy_document.lpa_rest_api_ip_restriction_policy[0].json] : []
  statement {
    sid    = "AllowExecuteByAllowedRoles"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = var.account.allowed_roles
    }
    actions   = ["execute-api:Invoke"]
    resources = ["arn:aws:execute-api:eu-west-?:${var.account.account_id}:*/*/*/*"]
  }
}

data "aws_iam_policy_document" "lpa_rest_api_ip_restriction_policy" {
  count = local.ip_restrictions_enabled ? 1 : 0
  statement {
    sid    = "DenyExecuteByNoneAllowedIPRanges"
    effect = "Deny"
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    actions       = ["execute-api:Invoke"]
    not_resources = ["arn:aws:execute-api:eu-west-?:${var.account.account_id}:*/*/*/healthcheck"]
    condition {
      test     = "NotIpAddress"
      variable = "aws:SourceIp"
      values   = sensitive(local.allow_list_mapping[var.account.account_mapping])
    }
  }
}

module "allow_list" {
  source = "git@github.com:ministryofjustice/opg-terraform-aws-moj-ip-allow-list.git?ref=v3.4.6"
}

