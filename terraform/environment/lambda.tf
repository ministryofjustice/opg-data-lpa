module "lambda_template_v1" {
  source                 = "./modules/lambda"
  environment            = local.environment
  aws_subnet_ids         = data.aws_subnet_ids.private.ids
  lambda_prefix          = "template"
  handler                = "app.template.lambda_handler"
  lambda_function_subdir = "template"
  tags                   = local.default_tags
  openapi_version        = "v1"
  rest_api               = aws_api_gateway_rest_api.template
  account                = local.account
}

//Modify here for new version - create new one. keep original
