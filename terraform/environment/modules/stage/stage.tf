locals {
  v1 = {
    flask_app_name : var.template_lambda.function_name
  }
  //Modify here for new version - uncomment below and modify accordingly
  //  v2 = {
  //    flask_app_name : var.template_lambda.function_name
  //  }
  //  stage_vars = var.openapi_version == "v1" ? local.v1 : local.v2
}

resource "aws_api_gateway_stage" "currentstage" {
  stage_name           = var.openapi_version
  depends_on           = [aws_cloudwatch_log_group.template_data]
  rest_api_id          = var.rest_api.id
  deployment_id        = aws_api_gateway_deployment.deploy.id
  xray_tracing_enabled = false
  tags                 = var.tags
  //Modify here for new version - replace with new code (comment out old code)
  variables = local.v1

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.template_data.arn
    format = join("", [
      "{\"requestId\":\"$context.requestId\",",
      "\"ip\":\"$context.identity.sourceIp\"",
      "\"caller\":\"$context.identity.caller\"",
      "\"user\":\"$context.identity.user\"",
      "\"requestTime\":\"$context.requestTime\"",
      "\"httpMethod\":\"$context.httpMethod\"",
      "\"resourcePath\":\"$context.resourcePath\"",
      "\"status\":\"$context.status\"",
      "\"protocol\":\"$context.protocol\"",
      "\"responseLength\":\"$context.responseLength\"}"
    ])
  }
}

resource "aws_cloudwatch_log_group" "template_data" {
  name              = "API-Gateway-Execution-Logs-${var.environment}-template-${var.openapi_version}"
  retention_in_days = 30
  tags              = var.tags
}
