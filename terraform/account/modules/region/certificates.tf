data "aws_route53_zone" "account_hosted_zone" {
  name     = "${var.account.opg_hosted_zone}."
  provider = aws.management
}

resource "aws_acm_certificate" "account_wildcard_cert" {
  domain_name               = "*.${data.aws_route53_zone.account_hosted_zone.name}"
  validation_method         = "DNS"
  subject_alternative_names = [data.aws_route53_zone.account_hosted_zone.name]
  lifecycle {
    create_before_destroy = true
  }
  region = var.region
}

resource "aws_route53_record" "account_wildcard_cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.account_wildcard_cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.account_hosted_zone.zone_id
  provider        = aws.management
}

resource "aws_acm_certificate_validation" "account_wildcard_cert" {
  certificate_arn         = aws_acm_certificate.account_wildcard_cert.arn
  validation_record_fqdns = [for record in aws_route53_record.account_wildcard_cert_validation : record.fqdn]
  region                  = var.region
}
