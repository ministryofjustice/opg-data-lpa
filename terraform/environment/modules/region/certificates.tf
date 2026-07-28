locals {
  a_record    = var.is_ephemeral ? lower("${var.environment}.${data.aws_route53_zone.environment_cert.name}") : lower(data.aws_route53_zone.environment_cert.name)
  certificate = var.is_ephemeral ? data.aws_acm_certificate.environment_cert[0] : aws_acm_certificate.environment_cert[0]
}

//===== Reference Zones from management =====

data "aws_route53_zone" "environment_cert" {
  name     = "${var.account.opg_hosted_zone}."
  provider = aws.management
}

//===== Create certificates for sub domains =====

resource "aws_acm_certificate" "environment_cert" {
  count                     = var.is_ephemeral ? 0 : 1
  domain_name               = "*.${data.aws_route53_zone.environment_cert.name}"
  validation_method         = "DNS"
  subject_alternative_names = [data.aws_route53_zone.environment_cert.name]
  lifecycle {
    create_before_destroy = true
  }
  region = var.region
}

data "aws_acm_certificate" "environment_cert" {
  count       = var.is_ephemeral ? 1 : 0
  domain      = "*.${trimsuffix(data.aws_route53_zone.environment_cert.name, ".")}"
  types       = ["AMAZON_ISSUED"]
  most_recent = true
}

resource "aws_route53_record" "validation" {
  count    = var.is_ephemeral ? 0 : 1
  name     = sort(aws_acm_certificate.environment_cert[0].domain_validation_options[*].resource_record_name)[0]
  type     = sort(aws_acm_certificate.environment_cert[0].domain_validation_options[*].resource_record_type)[0]
  zone_id  = data.aws_route53_zone.environment_cert.id
  records  = [sort(aws_acm_certificate.environment_cert[0].domain_validation_options[*].resource_record_value)[0]]
  ttl      = 60
  provider = aws.management
}
