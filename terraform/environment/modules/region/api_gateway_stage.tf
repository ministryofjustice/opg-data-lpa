resource "aws_api_gateway_stage" "current" {
  stage_name           = "v1"
  depends_on           = [aws_cloudwatch_log_group.lpa_data]
  rest_api_id          = aws_api_gateway_rest_api.lpa.id
  deployment_id        = aws_api_gateway_deployment.deploy.id
  xray_tracing_enabled = true
  //Modify here for new version - replace with new code (comment out old code)
  variables = {
    flask_app_name : aws_lambda_function.data_lpa.function_name
  }

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.lpa_data.arn
    format = join("", [
      "{\"requestId\":\"$context.requestId\",",
      "\"ip\":\"$context.identity.sourceIp\",",
      "\"caller\":\"$context.identity.caller\",",
      "\"user\":\"$context.identity.user\",",
      "\"requestTime\":\"$context.requestTime\",",
      "\"httpMethod\":\"$context.httpMethod\",",
      "\"resourcePath\":\"$context.resourcePath\",",
      "\"status\":\"$context.status\",",
      "\"protocol\":\"$context.protocol\",",
      "\"responseLength\":\"$context.responseLength\"}"
    ])
  }
  region = var.region
}

resource "aws_api_gateway_method_settings" "global_gateway_settings" {
  rest_api_id = aws_api_gateway_rest_api.lpa.id
  //Modify here for new version - replace with new code (comment out old code)
  stage_name  = aws_api_gateway_stage.current.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled = true
    logging_level   = "INFO"
  }
  region = var.region
}

resource "aws_cloudwatch_log_group" "lpa_data" {
  name              = "API-Gateway-Execution-Logs-${aws_api_gateway_rest_api.lpa.name}-v1"
  retention_in_days = 30
  region            = var.region
}

data "aws_wafv2_web_acl" "integrations" {
  name   = "integrations-${var.account.account_mapping}-${var.region}-web-acl"
  scope  = "REGIONAL"
  region = var.region
}

resource "aws_wafv2_web_acl_association" "api_gateway_stage" {
  resource_arn = aws_api_gateway_stage.current.arn
  web_acl_arn  = data.aws_wafv2_web_acl.integrations.arn
  region       = var.region
}

//Modify here for new version - replace with new code (comment out old code)
resource "aws_api_gateway_base_path_mapping" "mapping" {
  api_id      = aws_api_gateway_rest_api.lpa.id
  stage_name  = aws_api_gateway_stage.current.stage_name
  domain_name = aws_api_gateway_domain_name.lpa_data.domain_name
  base_path   = aws_api_gateway_stage.current.stage_name
  region      = var.region
}
