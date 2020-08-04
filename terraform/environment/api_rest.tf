data "template_file" "_" {
  template = local.openapispec
  vars     = local.api_template_vars
}

resource "aws_api_gateway_rest_api" "lpa" {
  name = "lpa-${local.environment}"
  body = data.template_file._.rendered

  endpoint_configuration {
    types = ["REGIONAL"]
  }
  lifecycle {
    ignore_changes = [
      policy,
      description
    ]
  }
  tags = local.default_tags
}
