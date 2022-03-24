locals {
  certificate_arn = local.branch_build_flag ? data.aws_acm_certificate.environment_cert[0].arn : aws_acm_certificate.environment_cert[0].arn
  certificate     = local.branch_build_flag ? data.aws_acm_certificate.environment_cert[0] : aws_acm_certificate.environment_cert[0]
}

resource "aws_api_gateway_method_settings" "global_gateway_settings" {
  rest_api_id = aws_api_gateway_rest_api.lpa.id
  //Modify here for new version - replace with new code (comment out old code)
  stage_name  = module.deploy_v1.stage.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled = true
    logging_level   = "INFO"
  }

}

resource "aws_api_gateway_domain_name" "lpa_data" {
  domain_name              = trimsuffix(local.a_record, ".")
  regional_certificate_arn = local.certificate_arn
  security_policy          = "TLS_1_2"

  depends_on = [local.certificate]
  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = local.default_tags
}

//Modify here for new version - create new one. keep original
module "deploy_v1" {
  source = "./modules/stage"

  account_name       = local.account.account_mapping
  api_name           = local.api_name
  aws_subnet_ids     = data.aws_subnet_ids.private.ids
  environment        = local.environment
  openapi_version    = "v1"
  region_name        = data.aws_region.region.name
  tags               = local.default_tags
  target_environment = local.account.target_environment
  vpc_id             = local.account.vpc_id
  //Modify here for new version - point to different version
  domain_name = aws_api_gateway_domain_name.lpa_data
  lpa_lambda  = module.lambda_lpa_v1.lambda
  rest_api    = aws_api_gateway_rest_api.lpa
}

//Modify here for new version - replace with new code (comment out old code)
resource "aws_api_gateway_base_path_mapping" "mapping" {
  api_id      = aws_api_gateway_rest_api.lpa.id
  stage_name  = module.deploy_v1.deployment.stage_name
  domain_name = aws_api_gateway_domain_name.lpa_data.domain_name
  base_path   = module.deploy_v1.deployment.stage_name
}
