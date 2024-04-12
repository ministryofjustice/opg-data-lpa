resource "aws_api_gateway_rest_api" "lpa" {
  name        = "lpa-${local.environment}"
  description = "API Gateway for LPA - ${local.environment}"
  body        = local.template_file

  endpoint_configuration {
    types = ["REGIONAL"]
  }
  tags = local.default_tags
  lifecycle {
    replace_triggered_by = [null_resource.open_api]
  }
}

resource "null_resource" "open_api" {
  triggers = {
    open_api_sha = local.open_api_sha
  }
}

locals {
  template_file = templatefile(local.openapi_spec, local.api_template_vars)
  open_api_sha  = substr(replace(base64sha256(local.template_file), "/[^0-9A-Za-z_]/", ""), 0, 5)
}
