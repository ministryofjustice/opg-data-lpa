module "lambda_lpa_v1" {
  source                 = "./modules/lambda"
  environment            = local.environment
  aws_subnet_ids         = data.aws_subnet.private.*.id
  lambda_prefix          = "lpa"
  handler                = "app.lpa.lambda_handler"
  lambda_function_subdir = "lpa"
  tags                   = local.default_tags
  openapi_version        = "v1"
  rest_api               = aws_api_gateway_rest_api.lpa
  account                = local.account
  redis_sg_id            = aws_security_group.lpa_redis_sg.id
  redis_url              = aws_route53_record.lpa_redis.name
}

//Modify here for new version - create new one. keep original
