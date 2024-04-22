locals {
  lambda = "${var.lambda_prefix}-${var.environment}-${var.openapi_version}"
}

resource "aws_cloudwatch_log_group" "lambda" {
  name = "/aws/lambda/${local.lambda}"
  tags = var.tags
}

resource "aws_lambda_function" "lambda_function" {
  filename         = data.archive_file.lambda_archive.output_path
  source_code_hash = data.archive_file.lambda_archive.output_base64sha256
  function_name    = local.lambda
  role             = aws_iam_role.lambda_role.arn
  handler          = var.handler
  runtime          = "python3.8"
  timeout          = 15
  depends_on       = [aws_cloudwatch_log_group.lambda]
  layers           = [aws_lambda_layer_version.lambda_layer.arn]
  vpc_config {
    subnet_ids = var.aws_subnet_ids
    security_group_ids = [
      data.aws_security_group.lambda_api_ingress.id,
      var.redis_sg_id
    ]
  }
  environment {
    variables = {
      SIRIUS_BASE_URL     = "http://api.${var.account.target_environment}.ecs"
      SIRIUS_API_VERSION  = "v1"
      ENVIRONMENT         = var.account.account_mapping
      LOGGER_LEVEL        = var.account.logger_level
      API_VERSION         = var.openapi_version
      SESSION_DATA        = var.account.session_data
      REQUEST_CACHING     = "enabled"
      REQUEST_CACHING_TTL = tostring(var.account.request_caching_ttl)
      REQUEST_TIMEOUT     = "10"
      REDIS_URL           = var.redis_url
    }
  }
  tracing_config {
    mode = "Active"
  }
  tags = var.tags
}

resource "aws_lambda_permission" "lambda_permission" {
  statement_id  = "AllowApiLPAGatewayInvoke_${var.environment}-${var.openapi_version}-${var.lambda_function_subdir}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${var.rest_api.execution_arn}/*/*/*"
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename         = data.archive_file.lambda_layer_archive.output_path
  source_code_hash = data.archive_file.lambda_layer_archive.output_base64sha256
  layer_name       = "lpa_requirements_${var.environment}"

  compatible_runtimes = ["python3.8"]

  lifecycle {
    ignore_changes = [
      source_code_hash
    ]
  }
}

data "local_file" "requirements" {
  filename = "../../lambda_functions/${var.openapi_version}/requirements/requirements.txt"
}

data "archive_file" "lambda_archive" {
  type        = "zip"
  source_dir  = "../../lambda_functions/${var.openapi_version}/functions/${var.lambda_function_subdir}"
  output_path = "./lambda_${var.lambda_function_subdir}.zip"
}

data "archive_file" "lambda_layer_archive" {
  type        = "zip"
  source_dir  = "../../lambda_functions/${var.openapi_version}/lambda_layers"
  output_path = "./lambda_layers_${var.lambda_function_subdir}_${substr(replace(base64sha256(data.local_file.requirements.content_base64), "/[^0-9A-Za-z_]/", ""), 0, 5)}.zip"
}
