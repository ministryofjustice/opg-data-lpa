resource "aws_route53_record" "environment_record" {
  name           = local.a_record
  type           = "A"
  zone_id        = data.aws_route53_zone.environment_cert.id
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
  regional_certificate_arn = local.certificate.arn
  security_policy          = "SecurityPolicy_TLS13_1_2_PFS_PQ_2025_09"
  endpoint_access_mode     = "BASIC"

  depends_on = [local.certificate]
  endpoint_configuration {
    types = ["REGIONAL"]
  }
  region = var.region
}
