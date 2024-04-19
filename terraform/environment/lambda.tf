module "lambda_lpa_v1" {
  source = "github.com/terraform-aws-modules/terraform-aws-lambda.git?ref=v7.2.6"

  function_name          = "lpa-${local.environment}-v1"
  handler                = "app.lpa.lambda_handler"
  vpc_subnet_ids         = data.aws_subnet.private.*.id
  vpc_security_group_ids = [aws_security_group.lpa_redis_sg.id, data.aws_security_group.lambda_api_ingress.id]
  tags                   = local.default_tags
  package_type           = "Image"
  image_uri              = var.lambda_image_uri
  tracing_mode           = "Active"
  timeout                = 15

  environment_variables = {
    SIRIUS_BASE_URL     = "http://api.${local.account.target_environment}.ecs"
    SIRIUS_API_VERSION  = "v1"
    ENVIRONMENT         = local.account.account_mapping
    LOGGER_LEVEL        = local.account.logger_level
    API_VERSION         = "v1"
    SESSION_DATA        = local.account.session_data
    REQUEST_CACHING     = "enabled"
    REQUEST_CACHING_TTL = tostring(local.account.request_caching_ttl)
    REQUEST_TIMEOUT     = "10"
    REDIS_URL           = aws_route53_record.lpa_redis.name
  }

  allowed_triggers = {
    APIGatewayTrigger = {
      statement_id = "AllowApiLPAGatewayInvoke_${local.environment}-v1-lpa"
      service      = "apigateway"
      source_arn   = "${aws_api_gateway_rest_api.lpa.execution_arn}/*/*/*"
    }
  }
}

moved {
  from = module.lambda_lpa_v1.aws_lambda_function.lambda_function
  to   = module.lambda_lpa_v1.aws_lambda_function.this[0]
}

moved {
  from = module.lambda_lpa_v1.aws_lambda_permission.lambda_permission
  to   = module.lambda_lpa_v1.aws_lambda_permission.unqualified_alias_triggers["APIGatewayTrigger"]
}

//Modify here for new version - create new one. keep original
