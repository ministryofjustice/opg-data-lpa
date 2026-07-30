removed {
  from = aws_acm_certificate.environment_cert
  lifecycle {
    destroy = false
  }
}
