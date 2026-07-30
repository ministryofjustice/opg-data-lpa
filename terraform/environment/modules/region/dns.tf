locals {
  a_record = var.is_ephemeral ? lower("${var.environment}.${var.account.opg_hosted_zone}") : var.account.opg_hosted_zone
}

data "aws_route53_zone" "account_hosted_zone" {
  name     = "${var.account.opg_hosted_zone}."
  provider = aws.management
}

data "aws_acm_certificate" "account_cert" {
  domain      = "*.${trimsuffix(data.aws_route53_zone.account_hosted_zone.name, ".")}"
  types       = ["AMAZON_ISSUED"]
  most_recent = true
  region      = var.region
}

resource "aws_route53_record" "environment_record" {
  name           = local.a_record
  type           = "A"
  zone_id        = data.aws_route53_zone.account_hosted_zone.id
  set_identifier = var.region

  alias {
    evaluate_target_health = true
    name                   = aws_api_gateway_domain_name.lpa_data.regional_domain_name
    zone_id                = aws_api_gateway_domain_name.lpa_data.regional_zone_id
  }

  weighted_routing_policy {
    weight = var.region_active ? 100 : 0
  }

  provider = aws.management
}

resource "aws_api_gateway_domain_name" "lpa_data" {
  domain_name              = trimsuffix(local.a_record, ".")
  regional_certificate_arn = data.aws_acm_certificate.account_cert.arn
  security_policy          = "SecurityPolicy_TLS13_1_2_PFS_PQ_2025_09"
  endpoint_access_mode     = "BASIC"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
  region = var.region
}
