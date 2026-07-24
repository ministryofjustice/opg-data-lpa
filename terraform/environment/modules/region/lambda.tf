resource "aws_lambda_function" "data_lpa" {
  function_name = "data-lpa-${var.environment}-v1"
  package_type  = "Image"
  image_uri     = "311462405659.dkr.ecr.${data.aws_region.current.region}.amazonaws.com/integrations/lpa-data-lambda:${var.lambda_image_tag}"
  role          = var.lambda_iam_role.arn
  timeout       = 20
  memory_size   = 256

  environment {
    variables = {
      SIRIUS_BASE_URL     = "http://api.${var.target_environment}.ecs"
      SIRIUS_API_VERSION  = "v1"
      ENVIRONMENT         = var.account.account_mapping
      LOGGER_LEVEL        = var.account.logger_level
      API_VERSION         = "v1"
      SESSION_DATA        = var.account.session_data
      REQUEST_CACHING     = "enabled"
      REQUEST_CACHING_TTL = tostring(var.account.request_caching_ttl)
      REQUEST_TIMEOUT     = "3"
      REDIS_URL           = var.region_active ? aws_elasticache_replication_group.lpa_redis[0].primary_endpoint_address : "PLACEHOLDER VALUE - REGION NOT ACTIVE"
    }
  }

  logging_config {
    log_format            = "JSON"
    application_log_level = "INFO"
    system_log_level      = "WARN"
  }

  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids = data.aws_subnets.application.ids
    security_group_ids = [
      aws_security_group.lambda.id,
      data.aws_security_group.lambda_sirius_api_ingress.id
    ]
  }
  region = var.region
}

resource "aws_lambda_permission" "invoke_from_api_gateway" {
  statement_id  = "AllowLambdaAPIGatewayInvocation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.data_lpa.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.tmp_execution_arn}/*/*/*"
  region        = var.region
}

